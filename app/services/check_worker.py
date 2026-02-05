from __future__ import annotations

import os
from pathlib import Path

from PySide6.QtCore import QObject, Signal

from app.utils.template_utils import is_valid_email, normalize_mapping, safe_format


class EmailCheckWorker(QObject):
    progress = Signal(int)
    log = Signal(str)
    finished = Signal(dict)
    failed = Signal(str)

    def __init__(
        self,
        excel_path: str,
        email_col: str,
        personal_folder: str | None,
        patterns: list[str],
        check_domain: bool,
    ):
        super().__init__()
        self.excel_path = excel_path
        self.email_col = email_col
        self.personal_folder = personal_folder
        self.patterns = patterns
        self.check_domain = check_domain

    def run(self):
        try:
            import pandas as pd

            df = pd.read_excel(self.excel_path)
            if df.empty:
                self.failed.emit("Το Excel δεν έχει γραμμές.")
                return

            cols = [str(c) for c in df.columns]
            if self.email_col not in cols:
                self.failed.emit(f"Η στήλη Email '{self.email_col}' δεν υπάρχει στο Excel.")
                return

            total = len(df)
            invalid_emails: list[tuple[int, str]] = []
            missing_pdfs_info: list[tuple[int, str, list[str]]] = []
            domain_cache: dict[str, bool] = {}
            dns_lookups = 0

            self.log.emit(f"[CHECK] Start | rows={total} | dns={self.check_domain}")

            for idx, (_, row) in enumerate(df.iterrows(), start=1):
                mapping = normalize_mapping(row.to_dict())
                email = (mapping.get(self.email_col, "") or "").strip()

                is_valid = is_valid_email(email)
                domain_ok = True
                domain = email.split("@", 1)[1].lower() if "@" in email else ""
                if self.check_domain and is_valid and domain:
                    if domain not in domain_cache:
                        dns_lookups += 1
                        domain_cache[domain] = is_valid_email(email, check_domain=True)
                    domain_ok = domain_cache[domain]

                if not (is_valid and (domain_ok if self.check_domain else True)):
                    invalid_emails.append((idx, email))

                if self.personal_folder and self.patterns:
                    missing_for_row: list[str] = []
                    for pat in self.patterns:
                        filename = safe_format(pat, mapping).strip()
                        filename = " ".join(filename.split())
                        if not filename:
                            missing_for_row.append(f"<empty-from-pattern: {pat}>")
                            continue
                        if not filename.lower().endswith(".pdf"):
                            filename += ".pdf"

                        fullpath = str(Path(self.personal_folder) / filename)
                        if not os.path.exists(fullpath):
                            missing_for_row.append(filename)

                    if missing_for_row:
                        missing_pdfs_info.append((idx, email, missing_for_row))

                self.progress.emit(int(idx / max(total, 1) * 100))

            lines: list[str] = []
            lines.append(f"Σύνολο γραμμών στο Excel: {total}")
            lines.append("")

            if invalid_emails:
                lines.append(f"Μη έγκυρα emails: {len(invalid_emails)}")
                lines.append("Πρώτα παραδείγματα:")
                for row_idx, email in invalid_emails[:10]:
                    lines.append(f"  - row {row_idx}: '{email}'")
            else:
                lines.append("Όλα τα emails φαίνονται έγκυρα.")
            lines.append("")

            if self.patterns and self.personal_folder:
                if missing_pdfs_info:
                    lines.append(f"Γραμμές με ΕΛΛΕΙΨΗ προσωπικών PDFs: {len(missing_pdfs_info)}")
                    lines.append("Πρώτα παραδείγματα:")
                    for row_idx, email, missing in missing_pdfs_info[:5]:
                        lines.append(f"  - row {row_idx} ({email or '-'}) λείπουν:")
                        for fname in missing[:5]:
                            lines.append(f"      • {fname}")
                else:
                    lines.append("Όλα τα προσωπικά PDFs βρέθηκαν για όλες τις γραμμές.")
            elif self.patterns and not self.personal_folder:
                lines.append("⚠️ Υπάρχουν patterns για personal PDFs αλλά δεν έχει επιλεγεί φάκελος personal PDFs.")
            else:
                lines.append("Δεν έχουν οριστεί patterns για προσωπικά PDFs (παράλειψη ελέγχου).")

            result_text = "\n".join(lines)
            self.progress.emit(100)
            self.finished.emit(
                {
                    "text": result_text,
                    "dns_lookups": dns_lookups,
                }
            )

        except Exception as exc:
            self.failed.emit(str(exc))
