import base64
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QMessageBox

from app.main_window import MainWindow
from app.services.mailer_worker import BulkMailerWorker
from app.utils.html_email import prepare_html_email


class HtmlImportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.image = b"inline-image-test"
        uri = base64.b64encode(self.image).decode("ascii")
        self.html = (
            '<html><head><meta charset="utf-8"></head><body>'
            '<table style="background:#1F4E79"><tr><td>Ελληνικό κείμενο</td></tr></table>'
            f'<img src="data:image/png;base64,{uri}"></body></html>'
        )

    def test_import_preserves_html_and_rejected_switch_keeps_it(self):
        window = MainWindow()
        try:
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "email.html"
                path.write_text(self.html, encoding="utf-8-sig")
                with patch("app.main_window.QFileDialog.getOpenFileName", return_value=(str(path), "")):
                    window.import_html()
                self.assertEqual(window._get_body_html(), self.html)
                self.assertTrue(window.ui.lblBody.isReadOnly())
                self.assertFalse(window.ui.btnBold.isEnabled())
                with patch("app.main_window.QMessageBox.question", return_value=QMessageBox.No):
                    window.use_text_editor()
                self.assertEqual(window._get_body_html(), self.html)
                with patch("app.main_window.QMessageBox.question", return_value=QMessageBox.Yes):
                    window.use_text_editor()
                self.assertIsNone(window._imported_html)
                self.assertFalse(window.ui.lblBody.isReadOnly())
                self.assertTrue(window.ui.btnBold.isEnabled())
        finally:
            window.close()

    def test_invalid_import_does_not_replace_existing_body(self):
        window = MainWindow()
        try:
            window._imported_html = self.html
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "broken.html"
                path.write_text('<img src="cid:missing">', encoding="utf-8")
                with patch("app.main_window.QFileDialog.getOpenFileName", return_value=(str(path), "")), \
                     patch("app.main_window.QMessageBox.critical") as error:
                    window.import_html()
                error.assert_called_once()
                self.assertEqual(window._get_body_html(), self.html)
        finally:
            window.close()

    def test_gmail_mime_preserves_styles_and_embeds_image(self):
        worker = BulkMailerWorker("", "", "", "", "draft", [], None, [], False)
        worker.gmail_user = "sender@example.com"
        with tempfile.TemporaryDirectory() as folder:
            pdf = Path(folder) / "attachment.pdf"
            pdf.write_bytes(b"ordinary-attachment")
            message = worker._build_gmail_message("reader@example.com", "Subject", self.html, [str(pdf)])
            parts = list(message.walk())
            image = next(p for p in parts if p.get_content_type() == "image/png")
            html = next(p for p in parts if p.get_content_type() == "text/html")
            self.assertEqual(image.get_payload(decode=True), self.image)
            self.assertEqual(image.get_content_disposition(), "inline")
            self.assertIn(f'cid:{image["Content-ID"][1:-1]}', html.get_content())
            self.assertIn('style="background:#1F4E79"', html.get_content())
            self.assertIn("Ελληνικό κείμενο", html.get_content())
            attachments = [p for p in parts if p.get_content_disposition() == "attachment"]
            self.assertEqual(len(attachments), 1)
            self.assertEqual(attachments[0].get_payload(decode=True), b"ordinary-attachment")

    def test_outlook_build_adds_inline_content_id_without_sending(self):
        mail = Mock()
        captured = []
        def add(Source):
            captured.append((Source, Path(Source).read_bytes()))
            return Mock()
        mail.Attachments.Add.side_effect = add
        BulkMailerWorker._set_outlook_html(mail, self.html)
        self.assertEqual(captured[0][1], self.image)
        self.assertFalse(Path(captured[0][0]).exists())
        self.assertIn('src="cid:fa-mailer-image-1@inline"', mail.HTMLBody)
        self.assertIn('style="background:#1F4E79"', mail.HTMLBody)
        mail.Send.assert_not_called()
        mail.Save.assert_not_called()

    def test_original_email_preserves_content_styles_links_and_logo(self):
        folder = Path(__file__).resolve().parents[1] / "email_import" / "elsekek"
        original = (folder / "original.html").read_text(encoding="utf-8")
        ready = (folder / "invitation.html").read_text(encoding="utf-8")
        html, images = prepare_html_email(ready)
        self.assertEqual(len(images), 1)
        restored = html.replace(f"cid:{images[0].cid}", "cid:image001.png@01DD528B.9317DF90")
        restored = restored.replace('<meta charset="utf-8">', "", 1)
        original = re.sub(r'(<li\b[^>]*>)\*\t', r'\1', original)
        original = original.replace(
            'Εμμ. Παπαδάκη 12, Τ.Κ. 14121, Ν. Ηράκλειο',
            'Δελφών 228 &amp; Μερκουρίου',
        ).replace('background:yellow;mso-highlight:yellow;', '')
        self.assertEqual(restored, original)
        self.assertEqual(images[0].data, (folder / "image001.png").read_bytes())

    def test_html_without_images_is_unchanged(self):
        html = '<p style="color:#1F4E79">Hello {Name}</p>'
        self.assertEqual(prepare_html_email(html), (html, []))


if __name__ == "__main__":
    unittest.main()
