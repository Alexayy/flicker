"""Run Flicker as a background service with a tray icon."""

from __future__ import annotations

import sys
from pathlib import Path
from threading import Thread

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QAction, QMenu, QSystemTrayIcon

from .keyboard_listener import start_listener


def _icon_path() -> Path:
    """Return the path to the installed icon."""
    dev_path = Path(__file__).resolve().parent.parent / "resources" / "flicker.png"
    if dev_path.exists():
        return dev_path
    return Path("/usr/share/flicker/flicker.png")


def main() -> None:
    """Start the hotkey listener and display a tray icon."""
    app = QApplication(sys.argv)

    # Start listener in a background thread so the Qt event loop can run
    listener_thread = Thread(target=start_listener, daemon=True)
    listener_thread.start()

    tray = QSystemTrayIcon(QIcon(str(_icon_path())), parent=None)
    tray.setToolTip("Flicker screenshot service")

    menu = QMenu()
    quit_action = QAction("Quit", menu)
    quit_action.triggered.connect(app.quit)  # type: ignore[arg-type]
    menu.addAction(quit_action)
    tray.setContextMenu(menu)
    tray.show()

    app.exec_()


if __name__ == "__main__":
    main()
