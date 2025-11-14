import curses
from core.cutils import addstr, getch, footer, move, reset_line


def account_settings(stdscr, username):

    #! Clear the terminal
    stdscr.clear()

    colors = [
        curses.color_pair(7) | curses.A_UNDERLINE,
        curses.color_pair(3),
    ]

    while True:
        addstr(stdscr, 0, 0, "seal", curses.color_pair(4) | curses.A_BOLD)
        addstr(stdscr, 0, 4, f" - Logged in as {username}", curses.A_BOLD)
        addstr(stdscr, 2, 0, "Account Settings", curses.A_BOLD)

        addstr(stdscr, 4, 1, "Go back", colors[0])
        addstr(stdscr, 6, 1, "Delete account", colors[1])
        footer(
            stdscr, "Use [▲] and [▼] arrow keys to navigate, and [Enter] to confirm."
        )

        ch = getch(stdscr)
        if ch == curses.KEY_RESIZE:
            continue

        if (
            ch == curses.KEY_DOWN
            and colors[0] == curses.color_pair(7) | curses.A_UNDERLINE
        ):
            colors[0] = curses.color_pair(5)
            colors[1] = curses.color_pair(8) | curses.A_UNDERLINE

        elif (
            ch == curses.KEY_UP
            and colors[1] == curses.color_pair(8) | curses.A_UNDERLINE
        ):
            colors[0] = curses.color_pair(7) | curses.A_UNDERLINE
            colors[1] = curses.color_pair(3)

        elif ch in (curses.KEY_ENTER, 10, 13):
            phrase = ""

            if colors[1] == curses.color_pair(8) | curses.A_UNDERLINE:
                addstr(stdscr, 8, 0, "Warning:", curses.color_pair(3) | curses.A_BOLD)
                addstr(
                    stdscr,
                    9,
                    0,
                    "You are about to delete your account. This action is ",
                    curses.color_pair(3),
                )
                addstr(
                    stdscr,
                    9,
                    53,
                    "irreversible",
                    curses.color_pair(3) | curses.A_UNDERLINE,
                )
                addstr(stdscr, 9, 65, "!", curses.color_pair(3))
                addstr(
                    stdscr,
                    10,
                    0,
                    "ALL stored passwords and data will be permanently lost.",
                    curses.color_pair(3),
                )
                addstr(
                    stdscr, 12, 0, "To confirm, please type your master password below."
                )
                footer(
                    stdscr,
                    "Press [ESC] to go back, and [Enter] to continue.",
                    attr=curses.A_UNDERLINE,
                )

                mp = ""
                while True:
                    addstr(stdscr, 14, 0, "> " + "*" * len(mp), reset=True)
                    move(stdscr, 14, 2 + len(mp))
                    stdscr.refresh()

                    ch = getch(stdscr)
                    if ch == curses.KEY_RESIZE:
                        continue

                    if ch in (curses.KEY_ENTER, 10, 13):
                        if mp == master_password:
                            #* Deleting account

                            from core.sqlutils import delete_user

                            delete_user(username)

                            reset_line(stdscr, 16, 0)
                            addstr(
                                stdscr,
                                16,
                                0,
                                "Account deleted successfully.",
                                curses.color_pair(2) | curses.A_BOLD,
                            )
                            addstr(stdscr, 17, 0, "Press any key to continue...")
                            getch(stdscr)

                            from core.utils import accounts_exist
                            from ui.normal_launch import normal_launch
                            from ui.first_time_launch import first_time_launch

                            if accounts_exist():
                                normal_launch(stdscr, "Welcome back, ")
                            else:
                                first_time_launch(stdscr)
                                normal_launch(stdscr, "Welcome, ")
                        else:
                            reset_line(stdscr, 16, 0)
                            addstr(
                                stdscr,
                                16,
                                0,
                                "Incorrect password. Account not deleted.",
                                curses.color_pair(3),
                            )
                            addstr(stdscr, 17, 0, "Press any key to go back...")
                            getch(stdscr)
                            stdscr.clear()
                            break

                    elif ch == 27: #* ESC key
                        stdscr.clear()
                        break

                    elif ch in (curses.KEY_BACKSPACE, 127, 8):
                        mp = mp[:-1]

                    elif (
                        (32 <= ch <= 126) and (ch not in [92, 39, 34]) and len(mp) < 64
                    ):
                        mp += chr(ch)
            
            else:
                break

    if colors[0] == curses.color_pair(7) | curses.A_UNDERLINE:
        stdscr.clear()
        return
