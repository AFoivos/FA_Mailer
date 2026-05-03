from __future__ import annotations

import sys
from pathlib import Path


def resource_path(relative_path: str) -> str:
    base_path = getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent)
    return str(Path(base_path) / relative_path)


WALLPAPER_PATH = resource_path("assets/wallpaper.png").replace("\\", "/")

APP_STYLE = """
QMainWindow {
    background-color: #eef3f9;
    background-image: url(assets/wallpaper.png);
    background-repeat: no-repeat;
    background-position: top center;
}

QMenuBar {
    background: transparent;
    border: none;
}

QStatusBar {
    background: rgba(245, 248, 252, 0.92);
    color: #556274;
    border-top: 1px solid rgba(107, 128, 153, 0.18);
}

QWidget#centralwidget {
    background: transparent;
    color: #172033;
    font-family: "Avenir Next", "Segoe UI", sans-serif;
    font-size: 14px;
}

QFrame#HeaderCard {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 rgba(12, 28, 56, 0.96),
        stop:1 rgba(24, 69, 132, 0.92)
    );
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 28px;
}

QLabel#lblEyebrow {
    color: rgba(219, 231, 255, 0.78);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

QLabel#lblHeroTitle {
    color: #f8fbff;
    font-size: 30px;
    font-weight: 800;
}

QLabel#lblHeroSubtitle {
    color: rgba(226, 235, 249, 0.9);
    font-size: 14px;
}

QFrame#SummaryCard,
QFrame#SidebarCard,
QFrame#ComposeCard,
QGroupBox,
QFrame#ModeCard,
QFrame#EditorCard {
    background: rgba(255, 255, 255, 0.93);
    border: 1px solid rgba(131, 148, 173, 0.20);
    border-radius: 24px;
}

QLabel#MetricLabel {
    color: #6d7890;
    font-size: 12px;
    font-weight: 600;
}

QLabel#MetricValue {
    color: #152033;
    font-size: 16px;
    font-weight: 700;
}

QLabel#PanelTitle {
    color: #172033;
    font-size: 20px;
    font-weight: 800;
}

QLabel#SectionTitle {
    color: #1a2740;
    font-size: 16px;
    font-weight: 700;
}

QLabel#FieldLabel {
    color: #4c5970;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
}

QLabel#HelperLabel {
    color: #66748d;
    font-size: 13px;
}

QGroupBox {
    margin-top: 10px;
    padding-top: 16px;
    font-weight: 700;
    color: #1a2740;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 18px;
    padding: 0 8px;
}

QLineEdit,
QComboBox,
QTextEdit,
QPlainTextEdit,
QListWidget {
    background: rgba(248, 250, 253, 0.98);
    color: #172033;
    border: 1px solid #d7deea;
    border-radius: 16px;
    padding: 10px 12px;
    selection-background-color: #c7ddff;
    selection-color: #152033;
}

QTextEdit,
QPlainTextEdit,
QListWidget {
    padding: 12px;
}

QLineEdit:focus,
QComboBox:focus,
QTextEdit:focus,
QPlainTextEdit:focus,
QListWidget:focus {
    border: 1px solid #2b6fff;
    background: #ffffff;
}

QComboBox {
    min-height: 22px;
}

QComboBox::drop-down {
    width: 28px;
    border: none;
}

QPushButton {
    background: rgba(236, 241, 249, 0.92);
    color: #20304c;
    border: 1px solid rgba(129, 147, 176, 0.24);
    border-radius: 14px;
    padding: 10px 16px;
    font-weight: 700;
}

QPushButton:hover {
    background: rgba(225, 234, 247, 1);
}

QPushButton:pressed,
QPushButton:checked {
    background: #dce8ff;
    border-color: #6e98ff;
}

QPushButton[variant="primary"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff8a3d, stop:1 #ff5a36);
    color: white;
    border: none;
    padding: 12px 22px;
}

QPushButton[variant="primary"]:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ff984f, stop:1 #ff6844);
}

QPushButton[variant="primary"]:pressed {
    background: #f35b2e;
}

QRadioButton,
QCheckBox {
    color: #20304c;
    spacing: 8px;
    font-weight: 600;
}

QRadioButton::indicator,
QCheckBox::indicator {
    width: 18px;
    height: 18px;
}

QRadioButton::indicator:unchecked,
QCheckBox::indicator:unchecked {
    border: 1px solid #a8b5ca;
    background: white;
    border-radius: 9px;
}

QRadioButton::indicator:checked,
QCheckBox::indicator:checked {
    border: 1px solid #2b6fff;
    background: #2b6fff;
    border-radius: 9px;
}

QCheckBox::indicator {
    border-radius: 5px;
}

QListWidget::item {
    padding: 8px 10px;
    border-radius: 10px;
    margin: 2px 0;
}

QListWidget::item:selected {
    background: #dbe8ff;
    color: #1d2c46;
}

QProgressBar {
    min-height: 16px;
    background: rgba(226, 233, 243, 0.86);
    border: none;
    border-radius: 8px;
    text-align: center;
    color: #20304c;
    font-weight: 700;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2b6fff, stop:1 #63b7ff);
    border-radius: 8px;
}

QSplitter::handle {
    background: transparent;
    width: 10px;
}

QMessageBox {
    background: #f8fafc;
}

QMessageBox QLabel {
    color: #172033;
}
"""

APP_STYLE = APP_STYLE.replace("assets/wallpaper.png", WALLPAPER_PATH)
