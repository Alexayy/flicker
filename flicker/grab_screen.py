import argparse
from .screenshot import (
    capture_selection,
    capture_full_screen,
    capture_window,
    capture_current_screen,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Take a screenshot")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--full', action='store_true', help='Grab all screens')
    group.add_argument('-c', '--screen', action='store_true', help='Grab the screen with the cursor')
    group.add_argument('-w', '--window', action='store_true', help='Grab the focused window')
    group.add_argument('-s', '--selection', action='store_true', help='Grab a selection (default)')
    args = parser.parse_args()

    if args.full:
        capture_full_screen()
    elif args.screen:
        capture_current_screen()
    elif args.window:
        capture_window()
    else:
        capture_selection()


if __name__ == '__main__':
    main()
