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


try:
    import curses
    import cryptography

    stdscr = curses.initscr()  #* Initialize the curses
    curses.noecho()  #* Hides user inputs
    curses.cbreak()  #* React to keys instantly
    stdscr.keypad(True)  #* Enable the keypad keys

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
            #* Define color number 10 as orange
            curses.init_color(10, 1000, 647, 0)
            curses.init_pair(1, 10, curses.COLOR_BLACK)
        else:
            stdscr.clear()
            stdscr.addstr("Terminal doesn't support custom colors.\n", curses.A_BOLD)

        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        #! Clear the terminal
        stdscr.clear()

        try:
            from master import create_master_password
            create_master_password(stdscr)

        except Exception as e:
            exception_handler(
                message="\033[96mMissing required file '\033[92mmaster.py\033[96m'. Please restore or re-download it.\033[0m",
                Exception=e,
            )

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
