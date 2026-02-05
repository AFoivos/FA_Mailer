from __future__ import annotations

import re
import socket

PLACEHOLDER_RE = re.compile(r"\{([A-Za-zΑ-Ωα-ω0-9_]+)\}")
EMAIL_RE = re.compile(
    r"^[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Z0-9-]+(?:\.[A-Z0-9-]+)+$",
    re.IGNORECASE,
)


def is_valid_email(value: str, check_domain: bool = False) -> bool:
    value = (value or "").strip()
    if not EMAIL_RE.fullmatch(value):
        return False

    if not check_domain:
        return True

    domain = value.split("@", 1)[1].strip().lower()
    if not domain:
        return False

    try:
        socket.getaddrinfo(domain, None)
        return True
    except OSError:
        return False


def normalize_mapping(row: dict) -> dict[str, str]:
    normalized = {}
    for key, value in row.items():
        key_str = str(key)
        if value is None:
            normalized[key_str] = ""
            continue

        value_str = str(value).strip()
        normalized[key_str] = "" if value_str.lower() == "nan" else value_str

    return normalized


def safe_format(template: str, mapping: dict) -> str:
    template = template or ""

    def replace(match):
        key = match.group(1)
        return str(mapping.get(key, "{" + key + "}"))

    return PLACEHOLDER_RE.sub(replace, template)
