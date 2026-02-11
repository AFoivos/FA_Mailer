import sys
import time
from pathlib import Path

"""
AF Mailer
Copyright (c) 2026 Φοίβος Γεώργιος Αμπατζής

All rights reserved.
Unauthorized copying, modification or distribution is prohibited.
"""

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QSplashScreen
from app.main_window import MainWindow
from app.ui_resources import resource_path


def main():
    app = QApplication(sys.argv)

    splash = None
    try:
        pm = QPixmap(resource_path("assets/front.png"))
        if not pm.isNull():
            # Make splash a bit smaller than the main window.
            target = QSize(int(986 * 0.90), int(791 * 0.90))
            pm = pm.scaled(target, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            splash = QSplashScreen(pm, Qt.WindowStaysOnTopHint)
            splash.show()
            app.processEvents()
    except Exception:
        splash = None

    start = time.perf_counter()
    w = MainWindow()

    def show_main():
        if splash is not None:
            splash.finish(w)
            splash.close()
        w.show()

    elapsed_ms = int((time.perf_counter() - start) * 1000)
    delay_ms = max(0, 5000 - elapsed_ms)
    QTimer.singleShot(delay_ms, show_main)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

# .\venv\Scripts\Activate.ps1
#  python -m app.main
