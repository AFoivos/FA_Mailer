from __future__ import annotations

import os
from pathlib import Path

from PySide6.QtCore import QObject, Signal

from app.utils.template_utils import is_valid_email, normalize_mapping, safe_format

"""
AF Mailer
Copyright (c) 2026 Φοίβος Γεώργιος Αμπατζής

All rights reserved.
Unauthorized copying, modification or distribution is prohibited.
"""


class BulkMailerWorker(QObject):
    progress = Signal(int)
    log = Signal(str)
    finished = Signal(dict)
    failed = Signal(str)

    def __init__(
        self,
        excel_path: str,
        email_col: str,
        subject_tpl: str,
        body_tpl: str,
        mode: str,
        common_paths: list[str],
        personal_folder: str | None,
        patterns: list[str],
        require_personal: bool,
    ):
        super().__init__()
        self.excel_path = excel_path
        self.email_col = email_col
        self.subject_tpl = subject_tpl
        self.body_tpl = body_tpl
        self.mode = mode
        self.common_paths = common_paths
        self.personal_folder = personal_folder
        self.patterns = patterns
        self.require_personal = require_personal

    def run(self):
        try:
            import pandas as pd
            import win32com.client as win32

            df = pd.read_excel(self.excel_path)
            if df.empty:
                self.failed.emit("Το Excel δεν έχει γραμμές.")
                return

            if self.email_col not in [str(c) for c in df.columns]:
                self.failed.emit(f"Η στήλη Email '{self.email_col}' δεν υπάρχει στο Excel.")
                return

            outlook = win32.Dispatch("Outlook.Application")

            total = len(df)
            ok = 0
            skipped = 0
            missing_personal = 0
            report_rows: list[dict[str, str]] = []

            self.log.emit(f"[RUN] Start | mode={self.mode} | rows={total}")

            for i, (_, row) in enumerate(df.iterrows(), start=1):
                mapping = normalize_mapping(row.to_dict())
                email = (mapping.get(self.email_col, "") or "").strip()

                if not is_valid_email(email):
                    skipped += 1
                    self.log.emit(f"[SKIP] invalid email: '{email}' (row {i})")
                    report_rows.append(
                        {
                            "row": str(i),
                            "email": email,
                            "status": "SKIP",
                            "reason": "invalid_email",
                            "error": "",
                            "mode": self.mode,
                        }
                    )
                    self.progress.emit(int(i / max(total, 1) * 100))
                    continue

                subject = safe_format(self.subject_tpl, mapping)
                body_html = safe_format(self.body_tpl, mapping)

                personal_files = []
                empty_personal_patterns: list[str] = []
                if self.personal_folder and self.patterns:
                    for pat in self.patterns:
                        filename = safe_format(pat, mapping).strip()
                        filename = " ".join(filename.split())
                        if not filename:
                            empty_personal_patterns.append(pat)
                            continue
                        if not filename.lower().endswith(".pdf"):
                            filename += ".pdf"
                        personal_files.append(str(Path(self.personal_folder) / filename))

                if self.require_personal:
                    missing = [p for p in personal_files if not os.path.exists(p)]
                    missing.extend([f"<empty-from-pattern: {p}>" for p in empty_personal_patterns])
                    if missing:
                        missing_personal += 1
                        self.log.emit(f"[MISS] personal PDFs missing (row {i}) -> SKIP email: {email}")
                        for missing_file in missing[:3]:
                            if missing_file.startswith("<empty-from-pattern:"):
                                self.log.emit(f"       - {missing_file}")
                            else:
                                self.log.emit(f"       - {Path(missing_file).name}")
                        report_rows.append(
                            {
                                "row": str(i),
                                "email": email,
                                "status": "SKIP",
                                "reason": "missing_required_personal_pdf",
                                "error": "; ".join(
                                    m if m.startswith("<empty-from-pattern:") else Path(m).name
                                    for m in missing
                                ),
                                "mode": self.mode,
                            }
                        )
                        self.progress.emit(int(i / max(total, 1) * 100))
                        continue

                try:
                    mail = outlook.CreateItem(0)
                    mail.To = email
                    mail.Subject = subject
                    mail.HTMLBody = body_html
                    missing_optional_personal: list[str] = []

                    for p in personal_files:
                        if os.path.exists(p):
                            mail.Attachments.Add(Source=p)
                        elif self.patterns:
                            self.log.emit(f"[WARN] missing personal pdf for {email}: {Path(p).name}")
                            missing_optional_personal.append(Path(p).name)

                    for p in self.common_paths:
                        if p and os.path.exists(p):
                            mail.Attachments.Add(Source=p)

                    if self.mode == "draft":
                        mail.Save()
                    else:
                        mail.Send()

                    ok += 1
                    self.log.emit(f"[OK] {email}")
                    report_rows.append(
                        {
                            "row": str(i),
                            "email": email,
                            "status": "DRAFT" if self.mode == "draft" else "SENT",
                            "reason": "optional_missing_personal_pdf" if missing_optional_personal else "",
                            "error": "; ".join(missing_optional_personal),
                            "mode": self.mode,
                        }
                    )

                except Exception as exc:
                    skipped += 1
                    self.log.emit(f"[ERR] row {i} email={email}: {exc}")
                    report_rows.append(
                        {
                            "row": str(i),
                            "email": email,
                            "status": "ERROR",
                            "reason": "send_error",
                            "error": str(exc),
                            "mode": self.mode,
                        }
                    )

                self.progress.emit(int(i / max(total, 1) * 100))

            self.progress.emit(100)
            self.log.emit(f"[RUN] END | ok={ok} skipped={skipped} missing_personal={missing_personal}")
            self.finished.emit(
                {
                    "ok": ok,
                    "skipped": skipped,
                    "missing_personal": missing_personal,
                    "mode": self.mode,
                    "rows": report_rows,
                    "subject_tpl": self.subject_tpl,
                }
            )

        except Exception as exc:
            self.failed.emit(str(exc))
