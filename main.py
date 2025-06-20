def exception_handler(message="Something went wrong.", Exception=None):
    print("\033[91m\033[1m[Fatal Error]\033[0m")  #* Red color
    print()
    print(message)
    print()
    if Exception:
        print("\033[93mFull error details:\033[0m")
        print(Exception)
        print()
    exit()


def rgb_to_curses_color(r, g, b):
    return int(r * 1000 / 255), int(g * 1000 / 255), int(b * 1000 / 255)


def exit_seal():
    #* Exit the program and restore terminal settings
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    exit()


def main(stdscr):
    #* Set up color pairs for colorful text
    curses.start_color()

    if curses.can_change_color():
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        curses.init_color(11, *rgb_to_curses_color(125, 229, 255))  #* teal
        curses.init_pair(4, 11, curses.COLOR_BLACK)

        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    else:
        stdscr.clear()
        exception_handler(
            message="\033[96mYour terminal does not support colored text.\033[0m"
        )

    #* Start SEAL

    try:
        from scripts.user import choose_username
        from scripts.encryption import encrypt, decrypt
        from scripts.menu import welcome

        welcome(stdscr)

        # username, password = choose_username(stdscr)
        # encrypt(
        #     username,
        #     password,
        #     [
        #         ["Outlook", "john@outlook.com", "InD9RQSVF0ZJ3up6", "azure"],
        #         ["Google", "john@gmail.com", "FtF9VDFnxMMgzVlE", "green"],
        #         ["Steam", "john@gmail.com", "lC3NdFOXXG9a9FHe", "blue"],
        #     ],
        # )
        # decrypt(username, password)

    except ModuleNotFoundError as e:
        missing_file = str(e).split("'")[1].split(".")[1]
        exception_handler(
            message=f"\033[96mMissing required file '\033[92mscripts/{missing_file}.py\033[96m'. Please restore or re-download it.\033[0m",
            Exception=e,
        )
    except Exception as e:
        exception_handler(Exception=e)


try:
    from sys import modules
    from os import path, system

    if "idlelib.run" in modules:
        #! Program runs itself in a terminal if it is run in IDLE
        #! This is because IDLE does not support curses, or colored text
        script = path.abspath(__file__)
        system(f"start \"\" py \"{script}\"")

    import curses
    import cryptography

    stdscr = curses.initscr()  #* Initialize the curses
    curses.noecho()  #* Hides user inputs
    curses.cbreak()  #* React to keys instantly
    stdscr.keypad(True)  #* Enable the keypad keys

    curses.wrapper(main)
    exit_seal()

except ModuleNotFoundError as e1:  #* Printing out a detailed, specific error message
    module_name = str(e1).split("'")[1]
    module_name = "windows_curses" if module_name == "_curses" else module_name
    try:
        if module_name == "windows_curses":
            from cryptography import __version__
        exception_handler(
            message=f"""\033[96mModule '\033[92m{module_name}\033[96m' not found.
You must install it using '\033[32mpip install \033[92m{module_name}\033[96m'\033[0m""",
            Exception=e1,
        )

    except ModuleNotFoundError as e2:
        exception_handler(
            message="""\033[96mBoth modules '\033[92mwindows_curses\033[96m' and '\033[92mcryptography\033[96m' were not found.
You must install them using '\033[32mpip install \033[92mwindows_curses\033[0m\033[32m,\033[92m \033[92mcryptography\033[0m\033[96m'\033[0m""",
        )

except Exception as e:
    exception_handler(Exception=e)
