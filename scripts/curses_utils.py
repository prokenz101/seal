import curses


def exit_curses(stdscr):
    #* Exit the program and restore terminal settings
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


def getch(stdscr):
    ch = stdscr.getch()
    if ch == curses.KEY_RESIZE:
        stdscr.clear()
        reset_line(stdscr, 0, 0)
        stdscr.addstr(
            0,
            0,
            "Please do not resize the terminal!",
            curses.color_pair(3) | curses.A_UNDERLINE | curses.A_BOLD,
        )
        stdscr.addstr(2, 0, "Press any key to continue...")
        getch(stdscr)
        stdscr.clear()

    return ch


def move(stdscr, y, x):
    max_y, max_x = stdscr.getmaxyx()
    if 0 <= y < max_y and 0 <= x < max_x:
        stdscr.move(y, x)
    else:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        print("\033[91m\033[1m[Fatal Error]\033[0m")
        print()
        print("Please enlarge your terminal window.\n")
        exit()


def addstr(stdscr, y, x, string, attr=curses.A_NORMAL):
    max_y, max_x = stdscr.getmaxyx()
    if 0 <= y < max_y and 0 <= x + len(string) < max_x:
        stdscr.addstr(y, x, string, attr)
    else:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        print("\033[91m\033[1m[Fatal Error]\033[0m")
        print()
        print("Please enlarge your terminal window.\n")
        exit()


def reset_line(stdscr, y, x):
    move(stdscr, y, x)
    stdscr.clrtoeol()


def footer(stdscr, message, attr=curses.A_NORMAL):
    max_y, max_x = stdscr.getmaxyx()
    reset_line(stdscr, max_y - 1, 0)
    addstr(stdscr, max_y - 1, 0, message, attr)
    stdscr.refresh()
