import curses
from core.cutils import addstr, move, footer, getch, addlines
from ui.mysql_setup import sql_warning
from ui.log_in import log_in

def normal_launch(stdscr, welcome="Welcome back, "):
    """Handle the normal launch experience for the user."""

    #! Clear the terminal
    stdscr.clear()

    colors = [
        curses.color_pair(7) | curses.A_UNDERLINE,
        curses.color_pair(5),
        curses.color_pair(5),
    ]

    while True:
        move(stdscr, 0, 0)
        stdscr.clrtoeol()
        addstr(stdscr, 1, 0, "███████╗███████╗ █████╗ ██╗     ", curses.color_pair(4))
        addstr(stdscr, 2, 0, "██╔════╝██╔════╝██╔══██╗██║     ", curses.color_pair(4))
        addstr(stdscr, 3, 0, "███████╗█████╗  ███████║██║     ", curses.color_pair(4))
        addstr(stdscr, 4, 0, "╚════██║██╔══╝  ██╔══██║██║     ", curses.color_pair(4))
        addstr(stdscr, 5, 0, "███████║███████╗██║  ██║███████╗", curses.color_pair(4))
        addstr(stdscr, 6, 0, "╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝", curses.color_pair(4))
        move(stdscr, 7, 0)
        stdscr.clrtoeol()
        addstr(stdscr, 8, 0, "Choose an option:")
        move(stdscr, 9, 0)
        stdscr.clrtoeol()
        addstr(stdscr, 10, 2, "Log in", colors[0])
        addstr(stdscr, 10, 11, "MySQL Setup", colors[1])
        addstr(stdscr, 10, 25, "Exit", colors[2])
        footer(
            stdscr, "Use [◀] and [▶] arrow keys to navigate, and [Enter] to confirm."
        )

        ch = getch(stdscr)  #* Wait for user key press
        if ch == curses.KEY_RESIZE:
            continue

        if ch == curses.KEY_RIGHT:
            index = colors.index(curses.color_pair(7) | curses.A_UNDERLINE)
            if index < 2:
                colors[index] = curses.color_pair(5)
                colors[index + 1] = curses.color_pair(7) | curses.A_UNDERLINE
        elif ch == curses.KEY_LEFT:
            index = colors.index(curses.color_pair(7) | curses.A_UNDERLINE)
            if index > 0:
                colors[index] = curses.color_pair(5)
                colors[index - 1] = curses.color_pair(7) | curses.A_UNDERLINE

        #* If Enter is pressed and requirement is met, exit loop
        elif ch in (curses.KEY_ENTER, 10, 13):
            break

    stdscr.clear()
    curses.curs_set(1)
    move(stdscr, 0, 0)
    if colors[0] == curses.color_pair(7) | curses.A_UNDERLINE:
        log_in(stdscr, welcome)
    elif colors[1] == curses.color_pair(7) | curses.A_UNDERLINE:
        setup_mysql(stdscr)
        normal_launch(stdscr)
    else:
        #! Exiting...
        pass
