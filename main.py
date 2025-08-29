from os import path, system
from sys import modules


def main(stdscr):
    """Main entry point."""

    #* Start SEAL
    from scripts.cutils import setup_colors

    setup_colors(stdscr)

    from scripts.menu import first_time_launch, normal_launch

    if accounts_exist():
        normal_launch(stdscr)
    else:
        first_time_launch(stdscr)


if __name__ == "__main__":
    try:
        from scripts.utils import exception_handler, is_all_modules_installed, accounts_exist

        if "idlelib.run" in modules:
            #! Program runs itself in a terminal if it is run in IDLE
            #! This is because IDLE does not support curses, or colored text
            script = path.abspath(__file__)  #* Path of main.py
            system(f'start "" py "{script}"')

        if is_all_modules_installed():
            import curses

            try:
                curses.wrapper(main)
            except curses.error:
                exception_handler("Terminal window is too small to display text.")

    except ModuleNotFoundError as e:
        #* Handle error if the user deletes necessary script files
        missing_file = str(e).split("'")[1].split(".")[1]
        print(
            f"\033[96mMissing required file '\033[92mscripts/{missing_file}.py\033[96m'. Please restore or re-download it.\033[0m"
        )
    except KeyboardInterrupt:
        print("\033[91m\033[1mExiting...\033[0m")
        print("Program interrupted by user.")
    except Exception as e:
        print("\033[91m\033[1m[Fatal Error]\033[0m")
        print("Something went wrong.\n")
        print(e)
