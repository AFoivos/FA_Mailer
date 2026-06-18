from __future__ import annotations

"""
AF Mailer
Copyright (c) 2026 Φοίβος Γεώργιος Αμπατζής

All rights reserved.
Unauthorized copying, modification or distribution is prohibited.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from PySide6.QtCore import QThread
from app.ui_main_window import Ui_MainWindow
from app.services.mailer_worker import BulkMailerWorker
from app.services.check_worker import EmailCheckWorker
from app.ui_resources import APP_STYLE, resource_path
from app.utils.template_utils import is_valid_email, normalize_mapping, safe_format
from PySide6.QtGui import QFont, QTextCharFormat, QTextCursor, QIcon
from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QInputDialog,
    QApplication,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPlainTextEdit,
    QTextEdit,
    QPushButton,
    QLabel,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(resource_path("assets/talis.ico")))
        self.setWindowTitle("AF Mailer")
        self.setMinimumSize(1280, 820)

        self.setStyleSheet(APP_STYLE)
        self._configure_window()
        self._setup_footer_copyright()
        log_font = QFont("SF Mono", 10)
        self.ui.txtLog.setFont(log_font)

        self.excel_path: str | None = None
        self.personal_pdf_folder: str | None = None
        self.common_attachments_paths: list[str] = []
        self.thread: QThread | None = None
        self.worker: BulkMailerWorker | None = None
        self.check_thread: QThread | None = None
        self.check_worker: EmailCheckWorker | None = None
        self._wire()
        self._refresh_mail_provider_ui()
        self._refresh_summary()

        self._log("Ready.")

    def _configure_window(self):
        self.ui.grpRun.setTitle("Campaign activity")
        self.ui.grpPersonalPdf.setTitle("Personalized attachments")
        self.ui.grpPlaceholders.setTitle("Available placeholders")

        self.ui.txtSubject.setTextMargins(10, 0, 10, 0)
        self.ui.lblBody.setViewportMargins(8, 8, 8, 8)
        self.ui.workspaceSplitter.setHandleWidth(14)

    def _setup_footer_copyright(self):
        if not hasattr(self.ui, "statusbar"):
            return

        footer = QLabel(
            "Copyright (c) 2026 FOIVOS GEORGIOS AMPATZIS. All rights reserved.",
            self,
        )
        footer.setStyleSheet("color: #35506f; font-size: 10px;")
        self.ui.statusbar.addPermanentWidget(footer, 1)
        self.ui.statusbar.setSizeGripEnabled(False)

    def _refresh_summary(self):
        excel_value = self._filename_only(self.excel_path) if self.excel_path else "No Excel loaded"
        email_column = (self.ui.comboEmailCol.currentText() or "").strip() or "Not selected"
        attachments = len(self.common_attachments_paths)

        if hasattr(self.ui, "lblSummaryExcelValue"):
            self.ui.lblSummaryExcelValue.setText(excel_value)
        if hasattr(self.ui, "lblSummaryRecipientsValue"):
            self.ui.lblSummaryRecipientsValue.setText(email_column)
        if hasattr(self.ui, "lblSummaryAttachmentsValue"):
            self.ui.lblSummaryAttachmentsValue.setText(f"{attachments} file{'s' if attachments != 1 else ''}")

    def _collect_pdf_patterns(self) -> list[str]:
        patterns: list[str] = []
        if not hasattr(self.ui, "listPdfPatterns"):
            return patterns

        for i in range(self.ui.listPdfPatterns.count()):
            pattern = (self.ui.listPdfPatterns.item(i).text() or "").strip()
            if pattern:
                patterns.append(pattern)
        return patterns

    def _set_action_buttons_enabled(self, enabled: bool):
        for name in ("btnRun", "btnPreview", "btnValidate", "btnCheck"):
            if hasattr(self.ui, name):
                getattr(self.ui, name).setEnabled(enabled)

    def _wire(self):
        self.ui.btnBrowseExcel.clicked.connect(self.pick_excel)
        self.ui.comboEmailCol.currentTextChanged.connect(self._refresh_summary)
        if hasattr(self.ui, "comboMailProvider"):
            self.ui.comboMailProvider.currentIndexChanged.connect(self._refresh_mail_provider_ui)

        self.ui.btnAddAttachments.clicked.connect(self.add_common_attachments)
        self.ui.btnClearAttachments.clicked.connect(self.clear_common_attachments)

        self.ui.btnBrowsePdfFolder.clicked.connect(self.pick_personal_pdf_folder)
        self.ui.btnAddPdfPattern.clicked.connect(self.add_pdf_pattern)
        self.ui.btnRemovePdfPattern.clicked.connect(self.remove_pdf_pattern)

        if hasattr(self.ui, "listPlaceholders"):
            self.ui.listPlaceholders.itemDoubleClicked.connect(self.copy_placeholder)

        self.ui.btnValidate.clicked.connect(self.validate_inputs)
        self.ui.btnPreview.clicked.connect(self.preview_first_row)
        self.ui.btnRun.clicked.connect(self.start_run_thread)
        
        if hasattr(self.ui, "btnCheck"):
            self.ui.btnCheck.clicked.connect(self.check_emails_and_pdfs)
            
        if hasattr(self.ui, "btnBold"):
            self.ui.btnBold.setCheckable(True)
            self.ui.btnBold.toggled.connect(self.toggle_bold)

        if hasattr(self.ui, "btnItalic"):
            self.ui.btnItalic.setCheckable(True)
            self.ui.btnItalic.toggled.connect(self.toggle_italic)

        if hasattr(self.ui, "btnUnderline"):
            self.ui.btnUnderline.setCheckable(True)
            self.ui.btnUnderline.toggled.connect(self.toggle_underline)

    def _log(self, msg: str):
        w = self.ui.txtLog
        if hasattr(w, "appendPlainText"):  
            w.appendPlainText(msg)
        else:  
            w.append(msg)
    
    def _merge_format_on_selection(self, fmt: QTextCharFormat):
        editor = self.ui.lblBody
        cursor = editor.textCursor()

        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)

        cursor.mergeCharFormat(fmt)
        editor.mergeCurrentCharFormat(fmt)


    @staticmethod
    def _filename_only(path: str) -> str:
        return Path(path).name

    @staticmethod
    def _foldername_only(path: str) -> str:
        p = Path(path)
        return p.name if p.name else str(p)

    @staticmethod
    def _safe_filename_part(value: str, fallback: str = "report") -> str:
        cleaned = re.sub(r'[<>:"/\\|?*\n\r\t]+', "_", (value or "").strip())
        cleaned = " ".join(cleaned.split())
        return cleaned[:80] if cleaned else fallback

    def _default_report_path(self, subject: str) -> Path:
        date_part = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        subject_part = self._safe_filename_part(subject, fallback="no_subject")
        filename = f"{date_part} - {subject_part}.xlsx"
        if self.excel_path:
            return Path(self.excel_path).resolve().parent / filename
        return Path.cwd() / filename

    def _save_send_report(self, rows: list[dict], subject: str) -> str | None:
        if not rows:
            return None
        try:
            import pandas as pd

            report_path = self._default_report_path(subject)
            report_df = pd.DataFrame(rows)
            report_df.to_excel(report_path, index=False)
            return str(report_path)
        except Exception as e:
            self._log(f"[REPORT] Failed to save send report: {e}")
            return None


    def pick_excel(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel",
            "",
            "Excel Files (*.xlsx *.xls)",
        )
        if not path:
            return

        self.excel_path = path
        self.ui.txtExcel.setText(self._filename_only(path))
        self._log(f"Excel selected: {self._filename_only(path)}")
        self._refresh_summary()

        self._load_excel_columns_and_placeholders(path)

    def _load_excel_columns_and_placeholders(self, excel_path: str):
        try:
            import pandas as pd

            df = pd.read_excel(excel_path, nrows=1)
            cols = [str(c) for c in df.columns]

            if hasattr(self.ui, "listPlaceholders"):
                self.ui.listPlaceholders.clear()
                for c in cols:
                    self.ui.listPlaceholders.addItem("{" + c + "}")
                self._log(f"Placeholders loaded: {len(cols)}")

            if hasattr(self.ui, "comboEmailCol"):
                self.ui.comboEmailCol.clear()
                self.ui.comboEmailCol.addItems(cols)

                preferred = ["e-mail", "email", "mail", "e_mail", "e mail", "e-mail address", "E MAIL", "E-MAIL", "EMAIL"]
                guess = None
                for c in cols:
                    if c.strip().lower() in preferred:
                        guess = c
                        break
                if guess:
                    self.ui.comboEmailCol.setCurrentText(guess)
                    self._log(f"Email column auto-selected: {guess}")
                self._refresh_summary()

        except Exception as e:
            QMessageBox.critical(self, "Excel error", str(e))
            self._log(f"[ERROR] Excel read failed: {e}")

    def _progress_set(self, pct: int):
        self.ui.progressBar.setValue(max(0, min(100, int(pct))))

    def _get_mode(self) -> str:
        if hasattr(self.ui, "radioDraft") and self.ui.radioDraft.isChecked():
            return "draft"
        return "send"

    def _get_mail_provider(self) -> str:
        if hasattr(self.ui, "comboMailProvider"):
            data = self.ui.comboMailProvider.currentData()
            if data:
                return str(data).strip().lower()
            text = (self.ui.comboMailProvider.currentText() or "").strip().lower()
            if "gmail" in text:
                return "gmail"
        return "outlook"

    def _get_gmail_credentials(self) -> tuple[str, str]:
        gmail_user = ""
        gmail_app_password = ""
        if hasattr(self.ui, "txtGmailUser"):
            gmail_user = (self.ui.txtGmailUser.text() or "").strip()
        if hasattr(self.ui, "txtGmailPassword"):
            gmail_app_password = (self.ui.txtGmailPassword.text() or "").strip().replace(" ", "")
        return gmail_user, gmail_app_password

    def _refresh_mail_provider_ui(self):
        provider = self._get_mail_provider()
        is_gmail = provider == "gmail"

        for name in ("lblGmailUser", "txtGmailUser", "lblGmailPassword", "txtGmailPassword", "lblGmailHint"):
            if hasattr(self.ui, name):
                getattr(self.ui, name).setVisible(is_gmail)

        if hasattr(self.ui, "radioDraft"):
            self.ui.radioDraft.setEnabled(not is_gmail)
            if is_gmail and self.ui.radioDraft.isChecked() and hasattr(self.ui, "radioSend"):
                self.ui.radioSend.setChecked(True)
            self.ui.radioDraft.setToolTip("Gmail SMTP supports Send now only." if is_gmail else "")

    def add_common_attachments(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select common attachments",
            "",
            "PDF Files (*.pdf);;All Files (*.*)",
        )
        if not paths:
            return

        added = 0
        for p in paths:
            p = str(Path(p).resolve())
            if p not in self.common_attachments_paths:
                self.common_attachments_paths.append(p)
                self.ui.listAttachments.addItem(self._filename_only(p))
                added += 1

        self._log(f"Common attachments: +{added} (total {len(self.common_attachments_paths)})")
        self._refresh_summary()

    def clear_common_attachments(self):
        self.common_attachments_paths.clear()
        self.ui.listAttachments.clear()
        self._log("Common attachments cleared.")
        self._refresh_summary()

    def pick_personal_pdf_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select personal PDF folder", "")
        if not folder:
            return

        self.personal_pdf_folder = str(Path(folder).resolve())
        self.ui.txtPdfFolderName.setText(self._foldername_only(self.personal_pdf_folder))
        self._log(f"Personal PDF folder: {self._foldername_only(self.personal_pdf_folder)}")

    def add_pdf_pattern(self):
        text, ok = QInputDialog.getText(
            self,
            "Add PDF pattern",
            "Δώσε pattern αρχείου (π.χ. {ΕΠΩΝΥΜΟ} {ΟΝΟΜΑ}.pdf):",
        )
        if not ok:
            return

        pattern = (text or "").strip()
        if not pattern:
            return
        
        if not pattern.lower().endswith(".pdf"):
            pattern += ".pdf"

        self.ui.listPdfPatterns.addItem(pattern)
        self._log(f"Added personal PDF pattern: {pattern}")

    def remove_pdf_pattern(self):
        lw = self.ui.listPdfPatterns
        row = lw.currentRow()
        if row < 0:
            QMessageBox.information(self, "Remove pattern", "Διάλεξε ένα pattern από τη λίστα.")
            return

        item = lw.item(row)
        pat = item.text() if item else ""
        lw.takeItem(row)
        self._log(f"Removed personal PDF pattern: {pat}")

    def copy_placeholder(self, item):
        text = item.text().strip()
        QApplication.clipboard().setText(text)
        self._log(f"Copied placeholder: {text}")

    def validate_inputs(self):
        errors = []
        warnings = []

        if not self.excel_path:
            errors.append("Δεν έχει επιλεγεί Excel.")
        else:
            p = Path(self.excel_path)
            if not p.exists():
                errors.append(f"Το Excel δεν βρέθηκε στο δίσκο: {p.name}")

        subject = (self.ui.txtSubject.text() or "").strip()
        if not subject:
            errors.append("Το Θέμα (Subject) είναι κενό.")

        body_widget = self.ui.lblBody
        if hasattr(body_widget, "toPlainText"):
            body = (body_widget.toPlainText() or "").strip()
        else:
            body = ""
        if not body:
            warnings.append("Το κείμενο email (Body) είναι κενό. (Αν θα μπεις μετά με template, αγνόησέ το.)")

        email_col = ""
        if hasattr(self.ui, "comboEmailCol"):
            email_col = (self.ui.comboEmailCol.currentText() or "").strip()
            if not email_col:
                errors.append("Δεν έχει επιλεγεί στήλη Email (Email column).")

        if hasattr(self.ui, "listPlaceholders"):
            if self.ui.listPlaceholders.count() == 0:
                warnings.append("Η λίστα placeholders είναι άδεια. (Επίλεξε Excel για να φορτώσουν οι στήλες.)")

        provider = self._get_mail_provider()
        if provider == "gmail":
            gmail_user, gmail_app_password = self._get_gmail_credentials()
            if not gmail_user:
                errors.append("Gmail address is required.")
            elif not is_valid_email(gmail_user):
                errors.append("Gmail address is not valid.")
            if not gmail_app_password:
                errors.append("Gmail app password is required.")
            if self._get_mode() == "draft":
                errors.append("Gmail SMTP supports Send now only. Select Send now or use Outlook for drafts.")

        patterns_count = 0
        if hasattr(self.ui, "listPdfPatterns"):
            patterns_count = self.ui.listPdfPatterns.count()

        require_personal = False
        if hasattr(self.ui, "chkRequirePersonalPdf"):
            require_personal = bool(self.ui.chkRequirePersonalPdf.isChecked())

        if patterns_count > 0 and not self.personal_pdf_folder:
            errors.append("Έχεις ορίσει personal PDF patterns αλλά δεν έχεις επιλέξει φάκελο personal PDFs.")

        if require_personal:
            if not self.personal_pdf_folder:
                errors.append("Το 'Απαραίτητο προσωπικό PDF' είναι ενεργό, αλλά δεν έχει επιλεγεί φάκελος personal PDFs.")
            if patterns_count == 0:
                errors.append("Το 'Απαραίτητο προσωπικό PDF' είναι ενεργό, αλλά δεν έχεις προσθέσει κανένα pattern.")

        if patterns_count > 0 and hasattr(self.ui, "listPdfPatterns"):
            for i in range(patterns_count):
                pat = (self.ui.listPdfPatterns.item(i).text() or "").strip()
                if not pat.lower().endswith(".pdf"):
                    warnings.append(f"Pattern #{i+1} δεν τελειώνει σε .pdf: {pat}")

        if hasattr(self, "common_attachments_paths"):
            if len(self.common_attachments_paths) == 0:
                warnings.append("Δεν έχεις βάλει attachments (προαιρετικό).")

        if errors:
            msg = "Βρέθηκαν σφάλματα:\n\n- " + "\n- ".join(errors)
            if warnings:
                msg += "\n\nΠροειδοποιήσεις:\n\n- " + "\n- ".join(warnings)

            QMessageBox.critical(self, "Validate: Σφάλμα", msg)
            self._log("[VALIDATE] FAIL")
            for e in errors:
                self._log(f"[ERR] {e}")
            for w in warnings:
                self._log(f"[WARN] {w}")
            return

        msg = "Validate OK.\n"
        if warnings:
            msg += "\nΠροειδοποιήσεις:\n\n- " + "\n- ".join(warnings)

        QMessageBox.information(self, "Validate: OK", msg)
        self._log("[VALIDATE] OK")
        for w in warnings:
            self._log(f"[WARN] {w}")

    def _get_body_text(self) -> str:
        w = self.ui.lblBody
        if hasattr(w, "toPlainText"):
            return (w.toPlainText() or "").strip()
        return ""
    
    def _get_body_html(self) -> str:
        w = self.ui.lblBody
        if hasattr(w, "toHtml"):
            return (w.toHtml() or "").strip()
        return ""

    def _show_preview_dialog(self, title: str, text: str):
        dlg = QDialog(self)
        dlg.setWindowTitle(title)
        dlg.resize(900, 700)

        layout = QVBoxLayout(dlg)

        box = QPlainTextEdit(dlg)
        box.setReadOnly(True)
        box.setPlainText(text)
        layout.addWidget(box)

        btn = QPushButton("Κλείσιμο", dlg)
        btn.clicked.connect(dlg.accept)
        layout.addWidget(btn)

        dlg.exec()

    def _show_email_preview_dialog(self, title: str, info_text: str, body_html: str):
        dlg = QDialog(self)
        dlg.setWindowTitle(title)
        dlg.resize(960, 760)

        layout = QVBoxLayout(dlg)

        info_box = QPlainTextEdit(dlg)
        info_box.setReadOnly(True)
        info_box.setPlainText(info_text)
        info_box.setMaximumHeight(280)
        layout.addWidget(info_box)

        html_box = QTextEdit(dlg)
        html_box.setReadOnly(True)
        html_box.setHtml(body_html or "")
        layout.addWidget(html_box)

        buttons = QHBoxLayout()
        close_btn = QPushButton("Κλείσιμο", dlg)
        close_btn.clicked.connect(dlg.accept)
        buttons.addStretch()
        buttons.addWidget(close_btn)
        layout.addLayout(buttons)

        dlg.exec()
        
    def preview_first_row(self):
        if not self.excel_path:
            QMessageBox.critical(self, "Preview error", "Δεν έχει επιλεγεί Excel.")
            return

        email_col = (self.ui.comboEmailCol.currentText() or "").strip()
        if not email_col:
            QMessageBox.critical(self, "Preview error", "Δεν έχει επιλεγεί στήλη Email.")
            return

        try:
            import pandas as pd
            df = pd.read_excel(self.excel_path, nrows=1)
            if df.empty:
                QMessageBox.critical(self, "Preview error", "Το Excel δεν έχει γραμμές.")
                return
            row = df.iloc[0].to_dict()
        except Exception as e:
            QMessageBox.critical(self, "Preview error", str(e))
            return

        mapping = normalize_mapping(row)

        subject_tpl = (self.ui.txtSubject.text() or "").strip()
        subject = safe_format(subject_tpl, mapping)

        body_tpl = self._get_body_html()
        body_html = safe_format(body_tpl, mapping)

        email = (mapping.get(email_col, "") or "").strip()

        common_names = [Path(p).name for p in getattr(self, "common_attachments_paths", [])]

        patterns = []
        if hasattr(self.ui, "listPdfPatterns"):
            for i in range(self.ui.listPdfPatterns.count()):
                pat = (self.ui.listPdfPatterns.item(i).text() or "").strip()
                if pat:
                    patterns.append(pat)

        folder_name = self._foldername_only(self.personal_pdf_folder) if self.personal_pdf_folder else "-"
        found, missing, expected = [], [], []

        if patterns:
            for pat in patterns:
                fname = safe_format(pat, mapping).strip()

                fname = " ".join(fname.split())

                if fname and not fname.lower().endswith(".pdf"):
                    fname += ".pdf"

                if not fname:
                    continue

                expected.append(fname)

                if self.personal_pdf_folder:
                    fullpath = str(Path(self.personal_pdf_folder) / fname)
                    if os.path.exists(fullpath):
                        found.append(fname)
                    else:
                        missing.append(fname)

        preview_text = []
        preview_text.append(f"Email (στήλη '{email_col}'):\n{email or '-'}")
        preview_text.append("\n" + "=" * 60 + "\n")
        preview_text.append("Subject:\n" + (subject or "-"))
        preview_text.append("\n" + "=" * 60 + "\n")
        preview_text.append("Body:\\n[HTML preview shown below]")
        preview_text.append("\n" + "=" * 60 + "\n")
        preview_text.append("Common attachments:\n" + ("\n".join(f"• {n}" for n in common_names) if common_names else "-"))
        preview_text.append("\n" + "=" * 60 + "\n")
        preview_text.append(f"Personal PDF folder: {folder_name}")

        if not patterns:
            preview_text.append("Personal PDFs patterns: -")
        else:
            if not self.personal_pdf_folder:
                preview_text.append("⚠️ Δεν έχει επιλεγεί φάκελος personal PDFs, οπότε δεν μπορεί να γίνει έλεγχος FOUND/MISSING.")
                preview_text.append("Αναμενόμενα filenames:\n" + "\n".join(f"• {n}" for n in expected))
            else:
                preview_text.append("FOUND:\n" + ("\n".join(f"✅ {n}" for n in found) if found else "-"))
                preview_text.append("MISSING:\n" + ("\n".join(f"❌ {n}" for n in missing) if missing else "-"))

        final_text = "\n".join(preview_text)

        self._log("[PREVIEW] OK (1st row)")
        self._show_email_preview_dialog("Preview (1st row)", final_text, body_html)
    
    def toggle_bold(self, checked: bool):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if checked else QFont.Normal)
        self._merge_format_on_selection(fmt)

    def toggle_italic(self, checked: bool):
        fmt = QTextCharFormat()
        fmt.setFontItalic(checked)
        self._merge_format_on_selection(fmt)

    def toggle_underline(self, checked: bool):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(checked)
        self._merge_format_on_selection(fmt)

    def check_emails_and_pdfs(self):
        if not self.excel_path:
            QMessageBox.critical(self, "Check error", "Δεν έχει επιλεγεί Excel.")
            return

        email_col = (self.ui.comboEmailCol.currentText() or "").strip()
        if not email_col:
            QMessageBox.critical(self, "Check error", "Δεν έχει επιλεγεί στήλη Email.")
            return

        dns_choice = QMessageBox.question(
            self,
            "Dry Run",
            "Enable domain DNS check for emails? (slower, more accurate)",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        check_domain = dns_choice == QMessageBox.StandardButton.Yes

        self._set_action_buttons_enabled(False)
        self._progress_set(0)
        self._log("[CHECK] Thread starting...")

        self.check_thread = QThread(self)
        self.check_worker = EmailCheckWorker(
            excel_path=self.excel_path,
            email_col=email_col,
            personal_folder=self.personal_pdf_folder,
            patterns=self._collect_pdf_patterns(),
            check_domain=check_domain,
        )
        self.check_worker.moveToThread(self.check_thread)

        self.check_thread.started.connect(self.check_worker.run)
        self.check_worker.progress.connect(self._progress_set)
        self.check_worker.log.connect(self._log)
        self.check_worker.finished.connect(self._on_check_finished)
        self.check_worker.failed.connect(self._on_check_failed)

        self.check_worker.finished.connect(self.check_thread.quit)
        self.check_worker.failed.connect(self.check_thread.quit)
        self.check_thread.finished.connect(self.check_worker.deleteLater)
        self.check_thread.finished.connect(self.check_thread.deleteLater)

        self.check_thread.start()

    def _on_check_finished(self, results: dict):
        self._set_action_buttons_enabled(True)
        self._progress_set(100)

        result_text = results.get("text", "")
        dns_lookups = results.get("dns_lookups", 0)
        self._log(f"[CHECK] Completed. dns_lookups={dns_lookups}")
        self._log(result_text)
        self._show_preview_dialog("Έλεγχος emails & προσωπικών PDFs", result_text)

    def _on_check_failed(self, err: str):
        self._set_action_buttons_enabled(True)
        self._log(f"[CHECK ERROR] {err}")
        QMessageBox.critical(self, "Check failed", err)
    def start_run_thread(self):
        if not self.excel_path:
            QMessageBox.critical(self, "Run error", "Δεν έχει επιλεγεί Excel.")
            return

        email_col = (self.ui.comboEmailCol.currentText() or "").strip()
        if not email_col:
            QMessageBox.critical(self, "Run error", "Δεν έχει επιλεγεί στήλη Email.")
            return

        subject_tpl = (self.ui.txtSubject.text() or "").strip()
        if not subject_tpl:
            QMessageBox.critical(self, "Run error", "Το Subject είναι κενό.")
            return

        body_tpl = self._get_body_html()

        mode = self._get_mode()  
        provider = self._get_mail_provider()
        gmail_user = ""
        gmail_app_password = ""
        if provider == "gmail":
            gmail_user, gmail_app_password = self._get_gmail_credentials()
            if not gmail_user:
                QMessageBox.critical(self, "Run error", "Gmail address is required.")
                return
            if not is_valid_email(gmail_user):
                QMessageBox.critical(self, "Run error", "Gmail address is not valid.")
                return
            if not gmail_app_password:
                QMessageBox.critical(self, "Run error", "Gmail app password is required.")
                return
            if mode == "draft":
                QMessageBox.critical(self, "Run error", "Gmail SMTP supports Send now only. Select Send now or use Outlook for drafts.")
                return

        require_personal = bool(self.ui.chkRequirePersonalPdf.isChecked()) if hasattr(self.ui, "chkRequirePersonalPdf") else False
        patterns = self._collect_pdf_patterns()

        if patterns and not self.personal_pdf_folder:
            QMessageBox.critical(self, "Run error", "Έχεις personal PDF patterns αλλά δεν έχεις επιλέξει φάκελο personal PDFs.")
            return
        if require_personal and (not self.personal_pdf_folder or not patterns):
            QMessageBox.critical(self, "Run error", "Το 'Απαραίτητο προσωπικό PDF' είναι ενεργό, αλλά λείπει φάκελος ή patterns.")
            return

        common_paths = list(getattr(self, "common_attachments_paths", []))

        provider_label = "Gmail" if provider == "gmail" else "Outlook"
        if QMessageBox.question(self, "Επιβεβαίωση", f"Provider: {provider_label}\nMode: {mode}\nΣυνέχεια;") != QMessageBox.Yes:
            return

        self._set_action_buttons_enabled(False)
        self._progress_set(0)
        self._log(f"[THREAD] Starting... provider={provider}")

        self.thread = QThread(self)
        self.worker = BulkMailerWorker(
            excel_path=self.excel_path,
            email_col=email_col,
            subject_tpl=subject_tpl,
            body_tpl=body_tpl,
            mode=mode,
            common_paths=common_paths,
            personal_folder=self.personal_pdf_folder,
            patterns=patterns,
            require_personal=require_personal,
            mail_provider=provider,
            gmail_user=gmail_user,
            gmail_app_password=gmail_app_password,
        )
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self._progress_set)
        self.worker.log.connect(self._log)
        self.worker.finished.connect(self._on_run_finished)
        self.worker.failed.connect(self._on_run_failed)

        self.worker.finished.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)
        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _on_run_finished(self, results: dict):
        self._set_action_buttons_enabled(True)

        ok = results.get("ok", 0)
        skipped = results.get("skipped", 0)
        miss = results.get("missing_personal", 0)
        mode = results.get("mode", "draft")
        provider = results.get("provider", "outlook")
        rows = results.get("rows", [])
        subject_for_report = results.get("subject_tpl", (self.ui.txtSubject.text() or "").strip())
        report_path = self._save_send_report(rows, subject_for_report)

        QMessageBox.information(
            self,
            "ΟΚ",
            (
                f"Ολοκληρώθηκε.\nProvider: {provider}\nMode: {mode}\nok={ok}\nskipped={skipped}\n"
                f"missing_personal={miss}\n"
                f"report={report_path or 'not saved'}"
            ),
        )
        if report_path:
            self._log(f"[REPORT] Send report saved: {report_path}")

    def _on_run_failed(self, err: str):
        self._set_action_buttons_enabled(True)

        self._log(f"[THREAD ERROR] {err}")
        QMessageBox.critical(self, "Run failed", err)
