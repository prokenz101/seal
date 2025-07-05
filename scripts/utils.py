
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


def exit_seal(stdscr):
    import curses
    #* Exit the program and restore terminal settings
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    exit()


def is_all_modules_installed():
    modules = {"windows_curses": False, "cryptography": False, "mysql.connector": False}
    #* Testing if individual modules are installed

    try:
        from curses import A_ALTCHARSET
        modules["windows_curses"] = True
    except ModuleNotFoundError:
        pass

    try:
        from cryptography import __version__
        modules["cryptography"] = True
    except ModuleNotFoundError:
        pass

    try:
        from mysql.connector import connect
        modules["mysql.connector"] = True
    except ModuleNotFoundError:
        pass

    if not all(modules.values()):
        print("\033[91m\033[1m[Fatal Error]\033[0m\n")
        print("\033[96mThe following required modules are not installed:\033[0m\n")
        for module in modules:
            if not modules[module]:
                print(f"- \033[93m{module}\033[0m")

        print("\n\033[96mPlease install them using the following command:\033[0m")
        print("'\033[92mpip install -r requirements.txt\033[0m'\n")

        return False

    return True


def reset_line(stdscr, y, x):
    stdscr.move(y, x)
    stdscr.clrtoeol()