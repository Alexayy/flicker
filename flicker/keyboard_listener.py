"""Keyboard hotkey listener for screenshot actions."""

from pynput import keyboard

from .screenshot import capture_full_screen, capture_screen, capture_selection


# Hotkeys are registered using the higher level GlobalHotKeys helper so we don't
# have to track key state manually.
HOTKEYS = {
    "<cmd>+<shift>+s": capture_selection,
    "<cmd>+<shift>+w": capture_screen,
    "<cmd>+<shift>+d": capture_full_screen,
    "<alt>+<shift>+s": capture_selection,
    "<alt>+<shift>+w": capture_screen,
    "<alt>+<shift>+d": capture_full_screen,
    "<f6>": capture_selection,
    "<f7>": capture_screen,
    "<f8>": capture_full_screen,
}


def start_listener() -> None:
    """Start listening for global hotkeys."""
    with keyboard.GlobalHotKeys(HOTKEYS) as listener:
        listener.join()


if __name__ == "__main__":
    start_listener()
