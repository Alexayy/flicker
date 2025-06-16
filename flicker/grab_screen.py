import argparse
from .screenshot import (
    capture_selection,
    capture_full_screen,
    capture_window,
    capture_current_screen,
    capture_monitor,
    list_monitors,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Take a screenshot")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--full', action='store_true', help='Grab all screens')
    group.add_argument('-c', '--screen', action='store_true', help='Grab the screen with the cursor')
    group.add_argument('-w', '--window', action='store_true', help='Grab the focused window')
    group.add_argument('-s', '--selection', action='store_true', help='Grab a selection (default)')
    group.add_argument('-m', '--monitor', type=int, metavar='N', help='Grab monitor N (1-based)')
    group.add_argument('-l', '--list-monitors', action='store_true', help='List available monitors')
    args = parser.parse_args()

    if args.list_monitors:
        list_monitors()
    elif args.monitor:
        capture_monitor(args.monitor)
    elif args.full:
        capture_full_screen()
    elif args.screen:
        capture_current_screen()
    elif args.window:
        capture_window()
    else:
        capture_selection()


if __name__ == '__main__':
    main()
