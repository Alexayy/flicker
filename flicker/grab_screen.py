import argparse
from .screenshot import capture_selection, capture_full_screen, capture_screen


def main() -> None:
    parser = argparse.ArgumentParser(description="Take a screenshot")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--full', action='store_true', help='Grab the entire screen')
    group.add_argument('-w', '--window', action='store_true', help='Grab the current window')
    group.add_argument('-s', '--selection', action='store_true', help='Grab a selection (default)')
    args = parser.parse_args()

    if args.full:
        capture_full_screen()
    elif args.window:
        capture_screen()
    else:
        capture_selection()


if __name__ == '__main__':
    main()
