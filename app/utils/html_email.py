from __future__ import annotations

import base64
import re
from dataclasses import dataclass
from html import unescape


@dataclass(frozen=True)
class InlineImage:
    cid: str
    data: bytes
    subtype: str
    filename: str


IMAGE_SOURCE = re.compile(
    r'(<img\b[^>]*?(?<![\w:-])src\s*=\s*)(["\'])(.*?)(\2)',
    re.IGNORECASE | re.DOTALL,
)
DATA_IMAGE = re.compile(
    r'data:image/(png|jpeg|gif);base64,([A-Za-z0-9+/=\s]+)', re.IGNORECASE
)


def prepare_html_email(body_html: str) -> tuple[str, list[InlineImage]]:
    """Keep HTML intact, replacing embedded images with email Content-IDs."""
    images: list[InlineImage] = []

    def replace(match: re.Match) -> str:
        source = unescape(match.group(3))
        data_match = DATA_IMAGE.fullmatch(source)
        if not data_match:
            if not source.lower().startswith(('https://', 'http://')):
                raise ValueError(
                    'Η εικόνα δεν είναι ενσωματωμένη στο HTML. '
                    'Χρησιμοποίησε HTML με εικόνες data:image/png, jpeg ή gif '
                    'ή με πλήρεις διαδικτυακούς συνδέσμους.'
                )
            return match.group(0)
        subtype = data_match.group(1).lower()
        data = base64.b64decode(re.sub(r'\s+', '', data_match.group(2)), validate=True)
        if not data:
            raise ValueError('Κενή ενσωματωμένη εικόνα στο HTML.')
        cid = f'fa-mailer-image-{len(images) + 1}@inline'
        images.append(InlineImage(cid, data, subtype, f'image-{len(images) + 1}.{subtype}'))
        return f'{match.group(1)}{match.group(2)}cid:{cid}{match.group(4)}'

    return IMAGE_SOURCE.sub(replace, body_html), images
