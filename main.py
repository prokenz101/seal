from os import path, system
from sys import modules


def main(stdscr):
    """Main entry point."""

    #* Start seal
    from core.cutils import setup_colors, check_terminal_size

    check_terminal_size(stdscr)
    setup_colors(stdscr)

    from ui.launch.first_time_launch import first_time_launch
    from ui.launch.normal_launch import normal_launch

    if accounts_exist():
        normal_launch(stdscr)
    else:
        first_time_launch(stdscr)
        normal_launch(stdscr, welcome="Welcome, ")


if __name__ == "__main__":
    try:
        from core.utils import (
            exception_handler,
            is_all_modules_installed,
            accounts_exist,
        )

        if "idlelib.run" in modules:
            #! Program runs itself in a terminal if it is run in IDLE
            #! This is because IDLE does not support curses, or colored text
            script = path.abspath(__file__) #* Path of main.py
            system(f'start "" py "{script}"')

        if is_all_modules_installed():
            import curses

            try:
                curses.wrapper(main)
            except curses.error:
                exception_handler("Terminal window is too small to display text.")

    except KeyboardInterrupt:
       #* ANSI codes for printing colors on modern terminals
        print("\033[91m\033[1mExiting...\033[0m")
        print("Program interrupted by user.")
    except Exception as e:
        print("\033[91m\033[1m[Fatal Error]\033[0m")
        print("Something went wrong.\n")
        print(e)
