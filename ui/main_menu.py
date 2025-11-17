import curses
from core.cutils import addlines, addstr, getch, footer
from ui.locker.locker import locker
from ui.account_settings import account_settings


def main_menu(stdscr, username, master_password):
    """Display the main menu after successful login."""

    #! Clear the terminal
    stdscr.clear()

    current_pos = "enter_seal"
    colors = [
        curses.color_pair(7),
        curses.color_pair(5),
        curses.color_pair(5),
    ]

    while True:
        addstr(stdscr, 0, 0, "seal", curses.color_pair(4) | curses.A_BOLD)
        addstr(stdscr, 0, 4, f" — Logged in as {username} — Main Menu", curses.A_BOLD)
        addstr(stdscr, 2, 0, "Choose an option:")
        addlines(
            stdscr,
            4,
            4,
            """------------------
|                |
|                |
|   Enter seal   |
|     Locker     |
|                |
|                |
------------------""",
            attr=colors[0],
        )
        addlines(
            stdscr,
            4,
            24,
            """-----------
|   Log   |
|   Out   |
-----------""",
            attr=colors[1],
        )
        addlines(
            stdscr,
            9,
            24,
            """------------
| Settings |
------------""",
            attr=colors[2],
        )

        footer(
            stdscr,
            "Use [◀], [▶], [▲], and [▼] arrow keys to navigate, and [Enter] to confirm.",
        )

        ch = getch(stdscr)
        if ch == curses.KEY_RESIZE:
            continue

        pos_idx = {"enter_seal": 0, "log_out": 1, "settings": 2}
        neighbors = {
            "enter_seal": {curses.KEY_RIGHT: "log_out"},
            "log_out": {curses.KEY_LEFT: "enter_seal", curses.KEY_DOWN: "settings"},
            "settings": {curses.KEY_LEFT: "enter_seal", curses.KEY_UP: "log_out"},
        }

        if ch in (curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN):
            nxt = neighbors.get(current_pos, {}).get(ch)
            if nxt and nxt != current_pos:
                current_pos = nxt

            for i in range(len(colors)):
                colors[i] = curses.color_pair(5)
            colors[pos_idx[current_pos]] = curses.color_pair(7)

        elif ch in (curses.KEY_ENTER, 10, 13):
            if current_pos == "settings":
                account_settings(stdscr, username, master_password)
            elif current_pos == "enter_seal":
                locker(stdscr, username, master_password)
            else:
                from ui.launch.normal_launch import normal_launch
                normal_launch(stdscr, welcome="Welcome back, ")
