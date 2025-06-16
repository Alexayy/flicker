"""Keyboard hotkey listener for screenshot actions.

The actual screenshot grabbing is delegated to the ``grab_screen`` CLI. This
ensures that any PyQt code runs in a separate process and avoids the common
``QApplication was not created in the main() thread`` errors.
"""

from __future__ import annotations

import subprocess
import sys

from pynput import keyboard


def _spawn_cli(flag: str | None = None) -> None:
    """Launch the grab-screen CLI in a new process."""
    cmd = [sys.executable, "-m", "flicker.grab_screen"]
    if flag:
        cmd.append(flag)
    subprocess.Popen(cmd)


# Hotkeys are registered using the higher level GlobalHotKeys helper so we don't
# have to track key state manually. Each hotkey simply calls the CLI with the
# appropriate flag.
HOTKEYS = {
    "<cmd>+<shift>+s": lambda: _spawn_cli("--selection"),
    "<cmd>+<shift>+w": lambda: _spawn_cli("--window"),
    "<cmd>+<shift>+d": lambda: _spawn_cli("--full"),
    "<alt>+<shift>+s": lambda: _spawn_cli("--selection"),
    "<alt>+<shift>+w": lambda: _spawn_cli("--window"),
    "<alt>+<shift>+d": lambda: _spawn_cli("--full"),
    "<f6>": lambda: _spawn_cli("--selection"),
    "<f7>": lambda: _spawn_cli("--screen"),
    "<f8>": lambda: _spawn_cli("--full"),
    "<f9>": lambda: _spawn_cli("--window"),
}


def start_listener() -> None:
    """Start listening for global hotkeys."""
    with keyboard.GlobalHotKeys(HOTKEYS) as listener:
        listener.join()


if __name__ == "__main__":
    start_listener()
