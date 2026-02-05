from __future__ import annotations

import sys
from pathlib import Path

"""
AF Mailer
Copyright (c) 2026 Φοίβος Γεώργιος Αμπατζής

All rights reserved.
Unauthorized copying, modification or distribution is prohibited.
"""


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent)
    return str(Path(base_path) / relative_path)


WALLPAPER_PATH = resource_path("assets/wallpaper.png").replace("\\", "/")

APP_STYLE = """
QMainWindow {
    background-image: url(assets/wallpaper.png);
    background-repeat: no-repeat;
    background-position: center;
    background-attachment: fixed;
}

QWidget#centralwidget {
    background-color: transparent;
    color: #1b2a3a;
    font-family: Segoe UI, Arial;
}

QLineEdit,
QTextEdit,
QPlainTextEdit,
QComboBox {
    background-color: #ffffff;
    border: 1px solid #b7cde8;
    border-radius: 5px;
    color: #1b2a3a;
}

QLineEdit:focus,
QTextEdit:focus,
QPlainTextEdit:focus,
QComboBox:focus {
    border: 1px solid #0d5eaf;
}

QListWidget {
    background-color: #ffffff;
    border: 1px solid #b7cde8;
    border-radius: 5px;
}

QListWidget::item:selected {
    background-color: #e6f0fb;
    color: #0d5eaf;
}

QPushButton {
    background-color: #e6f0fb;
    border: 1px solid #0d5eaf;
    border-radius: 5px;
    color: #0d5eaf;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #d4e6fb;
}

QPushButton:pressed {
    background-color: #0d5eaf;
    color: #ffffff;
}

QProgressBar {
    background-color: #ffffff;
    border: 1px solid #b7cde8;
    border-radius: 5px;
    text-align: center;
    color: #1b2a3a;
    font-weight: 600;
}

QProgressBar::chunk {
    background-color: #0d5eaf;
    border-radius: 5px;
}

QStatusBar {
    background-color: #e6f0fb;
    color: #0d5eaf;
}

#AppHeader {
    background-color: rgba(255, 255, 255, 180);
    border-bottom: 1px solid #c6dbf2;
}

#AppTitle {
    font-size: 18px;
    font-weight: 700;
    color: #0d5eaf;
}

QMessageBox {
    background-color: #ffffff;
}

QMessageBox QLabel {
    color: #1b2a3a;
}

QMessageBox QPushButton {
    background-color: #e6f0fb;
    border: 1px solid #0d5eaf;
    border-radius: 5px;
    color: #0d5eaf;
    font-weight: 600;
}

QMessageBox QPushButton:hover {
    background-color: #d4e6fb;
}

QMessageBox QPushButton:pressed {
    background-color: #0d5eaf;
    color: #ffffff;
}

#centralwidget {
    border-top: 1px solid rgba(13, 94, 175, 80);
}
"""

APP_STYLE = APP_STYLE.replace("assets/wallpaper.png", WALLPAPER_PATH)
