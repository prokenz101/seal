import curses
from core.cutils import addlines, addstr, move, footer, getch
from ui.username import choose_username
from ui.mysql_setup import setup_mysql


def first_time_launch(stdscr):
    """Handle the first-time launch experience for the user."""

    #! Clear the terminal
    stdscr.clear()

    colors = [curses.color_pair(7) | curses.A_UNDERLINE, curses.color_pair(5)]
    curses.curs_set(0)

    while True:
        addstr(stdscr, 0, 13, "Welcome to", curses.A_BOLD)
        addlines(
            stdscr,
            2,
            0,
            """                               ▄▄▄▄
                               ▀▀██     
 ▄▄█████▄   ▄████▄    ▄█████▄    ██     
 ██▄▄▄▄ ▀  ██▄▄▄▄██   ▀ ▄▄▄██    ██     
  ▀▀▀▀██▄  ██▀▀▀▀▀▀  ▄██▀▀▀██    ██     
 █▄▄▄▄▄██  ▀██▄▄▄▄█  ██▄▄▄███    ██▄▄▄  
  ▀▀▀▀▀▀     ▀▀▀▀▀    ▀▀▀▀ ▀▀     ▀▀▀▀""",
            curses.color_pair(4),
        )
        addstr(stdscr, 10, 0, "Choose an option:")
        addstr(stdscr, 12, 7, "Get Started", colors[0])
        addstr(stdscr, 12, 21, "Exit", colors[1])
        footer(
            stdscr, "Use [◀] and [▶] arrow keys to navigate, and [Enter] to confirm."
        )

        ch = getch(stdscr) #* Wait for user key press
        if ch == curses.KEY_RESIZE:
            continue

        if ch == curses.KEY_RIGHT:
            colors = [curses.color_pair(5), curses.color_pair(7) | curses.A_UNDERLINE]
        elif ch == curses.KEY_LEFT:
            colors = [curses.color_pair(7) | curses.A_UNDERLINE, curses.color_pair(5)]

       #* If Enter is pressed and requirement is met, exit loop
        elif ch in (curses.KEY_ENTER, 10, 13):
            break

    stdscr.clear()
    curses.curs_set(1)
    move(stdscr, 0, 0)
    if colors[0] == curses.color_pair(7) | curses.A_UNDERLINE:
        setup_mysql(stdscr)

        choose_username(stdscr)
    else:
        curses.endwin()
        exit()
        pass
