import os
import subprocess
import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication


def get_session_type():
    print(os.getenv('XDG_SESSION_TYPE'))
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

    if session_type == 'x11':
        cmd = ['import', '-window', 'root', full_path]
    elif session_type == 'wayland':
        cmd = ['grim', full_path]
    else:
        print("Unsupported session type.")
        return

    subprocess.run(cmd)
    print(f"Full screen screenshot saved as {full_path}")


def capture_selection():
    session_type = get_session_type()
    full_path = generate_file_path("selection")

    if session_type == 'x11':
        cmd = ['import', full_path]
        subprocess.run(cmd)
    elif session_type == 'wayland':
        cmd = f'grim -g "$(slurp)" {full_path}'
        subprocess.run(cmd, shell=True, executable='/bin/bash')
    else:
        print("Unsupported session type.")
        return

    print(f"Selection screenshot saved as {full_path}")


def capture_screen():
    session_type = get_session_type()

    if session_type not in ['x11', 'wayland']:
        print(f"Unsupported session type: {session_type}. This script is designed for X11 and Wayland.")
        sys.exit(1)

    home_dir = os.path.expanduser('~')
    save_path = os.path.join(home_dir, 'Pictures', 'FLICKERs')

    os.makedirs(save_path, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'screenshot_{timestamp}.png'
    full_path = os.path.join(save_path, filename)

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    screen = app.primaryScreen()
    screenshot = screen.grabWindow(0)
    screenshot.save(full_path, 'png')

    print(f"Screenshot saved as {full_path}")


if __name__ == "__main__":
    print("Session type:", get_session_type())
