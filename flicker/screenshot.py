"""Screenshot utilities supporting X11 and Wayland with PyQt fallbacks."""

import os
import subprocess
import sys
from datetime import datetime
from shutil import which

from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QWidget


def _open_file(filepath: str) -> None:
    """Try to open ``filepath`` with a desktop image viewer.

    This function attempts ``xdg-open`` (Linux) or ``open`` (macOS). If
    neither is available the path is printed so the user can open it
    manually.
    """
    print(f"Screenshot saved as {filepath}")
    commands = [['xdg-open', filepath], ['open', filepath]]
    for cmd in commands:
        try:
            subprocess.Popen(cmd)
            return
        except FileNotFoundError:
            continue
    print("Unable to automatically open the screenshot.")


def _cmd_exists(cmd: str) -> bool:
    """Return ``True`` if ``cmd`` exists on PATH."""
    return which(cmd) is not None


class _SnipWidget(QWidget):
    """Simple full-screen overlay for selecting a region."""

    def __init__(self) -> None:
        super().__init__()
        self.begin = QPoint()
        self.end = QPoint()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowState(self.windowState() | Qt.WindowFullScreen)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.CrossCursor)

    def paintEvent(self, event):  # type: ignore[override]
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2))
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        rect = QRect(self.begin, self.end)
        painter.fillRect(rect, Qt.transparent)
        painter.drawRect(rect)

    def mousePressEvent(self, event):  # type: ignore[override]
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):  # type: ignore[override]
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):  # type: ignore[override]
        self.end = event.pos()
        self.close()

    @property
    def selection(self) -> QRect:
        return QRect(self.begin, self.end).normalized()


def get_session_type():
    """Return the current desktop session type."""
    return os.getenv('XDG_SESSION_TYPE')


def generate_file_path(filename_prefix="screenshot"):
    home_dir = os.path.expanduser('~')
    save_path = os.path.join(home_dir, 'Pictures', 'FLICKERs')
    os.makedirs(save_path, exist_ok=True)
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"{filename_prefix}_{timestamp}.png"
    return os.path.join(save_path, filename)


def capture_full_screen():
    session_type = get_session_type()
    full_path = generate_file_path("full_screen")

    if session_type == "wayland" and _cmd_exists("grim"):
        subprocess.run(["grim", full_path])
    elif session_type == "x11" and _cmd_exists("import"):
        subprocess.run(["import", "-window", "root", full_path])
    else:
        # Fallback to PyQt grabbing
        app = QApplication.instance() or QApplication(sys.argv)
        screen = app.primaryScreen()
        screenshot = screen.grabWindow(0)
        screenshot.save(full_path, "png")

    _open_file(full_path)


def capture_selection():
    session_type = get_session_type()
    full_path = generate_file_path("selection")

    if session_type == "wayland" and _cmd_exists("grim") and _cmd_exists("slurp"):
        cmd = f'grim -g "$(slurp)" {full_path}'
        subprocess.run(cmd, shell=True, executable="/bin/bash")
    elif session_type == "x11" and _cmd_exists("import"):
        subprocess.run(["import", full_path])
    else:
        app = QApplication.instance() or QApplication(sys.argv)
        screen = app.primaryScreen()
        overlay = _SnipWidget()
        overlay.show()
        app.exec_()
        rect = overlay.selection
        if rect.width() and rect.height():
            screenshot = screen.grabWindow(0, rect.x(), rect.y(), rect.width(), rect.height())
            screenshot.save(full_path, "png")
        else:
            print("Selection cancelled.")
            return

    _open_file(full_path)


def capture_screen():
    session_type = get_session_type()
    full_path = generate_file_path("screenshot")

    if session_type == "wayland" and _cmd_exists("grim"):
        subprocess.run(["grim", full_path])
    elif session_type == "x11" and _cmd_exists("import"):
        subprocess.run(["import", full_path])
    else:
        app = QApplication.instance() or QApplication(sys.argv)
        screen = app.primaryScreen()
        screenshot = screen.grabWindow(0)
        screenshot.save(full_path, "png")

    _open_file(full_path)


if __name__ == "__main__":
    print("Session type:", get_session_type())
