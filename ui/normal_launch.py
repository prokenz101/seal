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
        addlines(
            stdscr,
            1,
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
        addstr(stdscr, 9, 0, "Choose an option:")
        move(stdscr, 10, 0)
        stdscr.clrtoeol()
        addstr(stdscr, 11, 1, "Log In", colors[0])
        addstr(stdscr, 13, 1, "Add Account", colors[1])
        addstr(stdscr, 15, 1, "MySQL Setup", colors[2])
        addstr(stdscr, 17, 1, "Exit", colors[3])
        footer(
            stdscr, "Use [▲] and [▼] arrow keys to navigate, and [Enter] to confirm."
        )

        ch = getch(stdscr)  #* Wait for user key press
        if ch == curses.KEY_RESIZE:
            continue

        if ch == curses.KEY_DOWN:
            index = colors.index(curses.color_pair(7) | curses.A_UNDERLINE)
            if index < 3:
                colors[index] = curses.color_pair(5)
                colors[index + 1] = curses.color_pair(7) | curses.A_UNDERLINE
        elif ch == curses.KEY_UP:
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
        from ui.username import choose_username

        choose_username(stdscr)
        normal_launch(stdscr)

    elif colors[2] == curses.color_pair(7) | curses.A_UNDERLINE:
        sql_warning(stdscr)
        normal_launch(stdscr)

    else:
        #! Exiting...
        curses.endwin()
        exit()
        pass
