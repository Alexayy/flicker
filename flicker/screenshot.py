"""Screenshot utilities supporting X11 and Wayland with PyQt fallbacks."""

import os
import subprocess
import sys
from datetime import datetime
from shutil import which

from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QColor, QPainter, QPen, QCursor, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget


def _notify(msg: str) -> None:
    """Send a desktop notification if possible."""
    commands = [['notify-send', msg], ['osascript', '-e', f'display notification "{msg}"']]
    for cmd in commands:
        try:
            subprocess.Popen(cmd)
            return
        except FileNotFoundError:
            continue
    print(msg)


def _copy_to_clipboard(filepath: str) -> None:
    """Copy the image at ``filepath`` to the clipboard."""
    app = QApplication.instance() or QApplication(sys.argv)
    pixmap = QPixmap(filepath)
    if not pixmap.isNull():
        app.clipboard().setPixmap(pixmap)


def _open_file(filepath: str) -> None:
    """Try to open ``filepath`` with a desktop image viewer.

    This function attempts ``xdg-open`` (Linux) or ``open`` (macOS). If
    neither is available the path is printed so the user can open it
    manually.
    """
    print(f"Screenshot saved as {filepath}")
    _copy_to_clipboard(filepath)
    _notify(f"Screenshot saved as {filepath}")
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
    """Transparent overlay for selecting a region on any screen."""

    def __init__(self) -> None:
        super().__init__()
        self.begin = QPoint()
        self.end = QPoint()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.CrossCursor)
        # Cover the whole virtual desktop so selections can span monitors
        geometry = QApplication.primaryScreen().virtualGeometry()
        self.setGeometry(geometry)

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
        rect = QRect(self.begin, self.end).normalized()
        rect.moveTopLeft(self.mapToGlobal(rect.topLeft()))
        return rect


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


def list_monitors() -> None:
    """Print available monitors and their geometries."""
    app = QApplication.instance() or QApplication(sys.argv)
    for idx, screen in enumerate(app.screens(), 1):
        geom = screen.geometry()
        print(f"{idx}: {screen.name()} {geom.width()}x{geom.height()} @({geom.x()},{geom.y()})")


def capture_monitor(index: int) -> None:
    """Capture a specific monitor by 1-based index."""
    app = QApplication.instance() or QApplication(sys.argv)
    screens = app.screens()
    if index < 1 or index > len(screens):
        print(f"Monitor {index} not available")
        return
    screen = screens[index - 1]
    full_path = generate_file_path(f"monitor{index}")
    screenshot = screen.grabWindow(0)
    screenshot.save(full_path, "png")
    _open_file(full_path)


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
        screens = app.screens()
        if len(screens) == 1:
            screenshot = screens[0].grabWindow(0)
            screenshot.save(full_path, "png")
        else:
            geom = app.primaryScreen().virtualGeometry()
            pixmap = QPixmap(geom.size())
            painter = QPainter(pixmap)
            for scr in screens:
                part = scr.grabWindow(0)
                painter.drawPixmap(scr.geometry().topLeft() - geom.topLeft(), part)
            painter.end()
            pixmap.save(full_path, "png")

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
        overlay = _SnipWidget()
        overlay.show()
        app.exec_()
        rect = overlay.selection
        if rect.width() and rect.height():
            screens = app.screens()
            pixmap = QPixmap(rect.size())
            painter = QPainter(pixmap)
            for scr in screens:
                geom = scr.geometry()
                inter = rect.intersected(geom)
                if not inter.isNull():
                    gx = inter.x() - geom.x()
                    gy = inter.y() - geom.y()
                    part = scr.grabWindow(0, gx, gy, inter.width(), inter.height())
                    painter.drawPixmap(inter.topLeft() - rect.topLeft(), part)
            painter.end()
            pixmap.save(full_path, "png")
        else:
            print("Selection cancelled.")
            return

    _open_file(full_path)


def capture_current_screen() -> None:
    """Capture the display containing the mouse pointer."""
    app = QApplication.instance() or QApplication(sys.argv)
    cursor_pos = QCursor.pos()
    screen = app.screenAt(cursor_pos)
    if screen is None:
        screen = app.primaryScreen()
    full_path = generate_file_path("screen")
    screenshot = screen.grabWindow(0)
    screenshot.save(full_path, "png")
    _open_file(full_path)


def capture_window() -> None:
    """Capture the currently focused window if possible."""
    session_type = get_session_type()
    full_path = generate_file_path("window")

    if session_type == "x11" and _cmd_exists("import") and _cmd_exists("xdotool"):
        try:
            win_id = (
                subprocess.check_output(["xdotool", "getactivewindow"]).decode().strip()
            )
            subprocess.run(["import", "-window", win_id, full_path])
        except subprocess.CalledProcessError:
            pass
        else:
            _open_file(full_path)
            return

    # Fallback to grabbing the screen region of the active window using PyQt
    app = QApplication.instance() or QApplication(sys.argv)
    widget = app.activeWindow()
    screen = app.primaryScreen()
    if widget:
        geo = widget.frameGeometry()
        screen = app.screenAt(geo.center()) or screen
        gx = geo.x() - screen.geometry().x()
        gy = geo.y() - screen.geometry().y()
        screenshot = screen.grabWindow(0, gx, gy, geo.width(), geo.height())
    else:
        screenshot = screen.grabWindow(0)
    screenshot.save(full_path, "png")
    _open_file(full_path)


# Backwards compatibility
def capture_screen() -> None:
    capture_window()


if __name__ == "__main__":
    print("Session type:", get_session_type())
