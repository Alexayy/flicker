from pynput import keyboard
from screenshot import capture_full_screen, capture_selection, capture_screen

current_keys = set()


def on_press(key):
    current_keys.add(key)

    if {keyboard.Key.alt_l, keyboard.Key.shift,
        keyboard.KeyCode.from_char('s')} <= current_keys or key == keyboard.Key.f9:
        print("Capturing selection...")
        capture_selection()

    elif {keyboard.Key.alt_l, keyboard.Key.shift,
          keyboard.KeyCode.from_char('w')} <= current_keys or key == keyboard.Key.f10:
        print("Capturing screen...")
        capture_screen()

    elif {keyboard.Key.alt_l, keyboard.Key.shift,
          keyboard.KeyCode.from_char('d')} <= current_keys or key == keyboard.Key.f11:
        print("Capturing full screen...")
        capture_full_screen()


def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass


def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    start_listener()
