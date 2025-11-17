import curses
import os
from core.cutils import addstr, getch, footer, move, reset_footer, reset_line
from core.sqlutils import change_username, change_master_password
from ui.setup.master_password import choose_master_password
from ui.setup.username import choose_username


def account_settings(stdscr, username, master_password):

    #! Clear the terminal
    stdscr.clear()

    colors = [
        [curses.color_pair(7) | curses.A_UNDERLINE, curses.color_pair(5), 0],
        [curses.color_pair(7) | curses.A_UNDERLINE, curses.color_pair(5), 1],
        [curses.color_pair(9) | curses.A_UNDERLINE, curses.color_pair(1), 1],
        [curses.color_pair(8) | curses.A_UNDERLINE, curses.color_pair(3), 1],
    ]
    current_pos = 0
    continued = None
    new_username = ""
    new_password = ""

    while True:
        addstr(stdscr, 0, 0, "seal", curses.color_pair(4) | curses.A_BOLD)
        addstr(
            stdscr,
            0,
            4,
            f" — Logged in as {username if new_username == '' else new_username} — Account Settings",
            curses.A_BOLD,
        )
        addstr(stdscr, 2, 0, "Options:", curses.A_BOLD)

        addstr(stdscr, 4, 1, "Go back", colors[0][colors[0][2]])
        addstr(stdscr, 6, 1, "Change username", colors[1][colors[1][2]])

        addstr(
            stdscr,
            8,
            1,
            "Change master password",
            colors[2][colors[2][2]],
            reset=True,
        )
        reset_line(stdscr, 9, 0)
        if not continued:
            addstr(stdscr, 10, 1, "Delete account", colors[3][colors[3][2]], reset=True)
            footer(
                stdscr,
                "Use [▲] and [▼] arrow keys to navigate, and [Enter] to confirm.",
            )

            ch = getch(stdscr)
        else:
            ch = continued

        if ch == curses.KEY_RESIZE:
            continue

        if ch == curses.KEY_DOWN:
            if current_pos < 3:
                colors[current_pos][2] = 1
                current_pos += 1
                colors[current_pos][2] = 0

        elif ch == curses.KEY_UP:
            if current_pos > 0:
                colors[current_pos][2] = 1
                current_pos -= 1
                colors[current_pos][2] = 0

        elif ch in (curses.KEY_ENTER, 10, 13):
            if current_pos == 0:  #* Go back
                stdscr.clear()
                break

            elif current_pos == 1:  #* Change username
                if not continued:
                    new_username = choose_username(stdscr, username_only=True)
                    if new_username is None:
                        continue

                    stdscr.clear()
                    continued = curses.KEY_ENTER
                else:
                    continued = None

                    #* Changing username
                    change_username(username, new_username)

                    reset_line(stdscr, 10, 0)
                    addstr(
                        stdscr,
                        8,
                        0,
                        "  New username will be set to:",
                        curses.color_pair(2) | curses.A_BOLD,
                        reset=True,
                    )
                    addstr(stdscr, 8, 31, new_username, curses.A_BOLD)
                    addstr(
                        stdscr,
                        10,
                        0,
                        "  To apply changes, please restart the application.",
                        curses.A_BOLD,
                        reset=True,
                    )
                    addstr(stdscr, 11, 0, "  Press any key to exit...", reset=True)
                    getch(stdscr)

                    curses.endwin()
                    exit()

            elif current_pos == 2:  #* Change master password
                addstr(
                    stdscr,
                    10,
                    0,
                    "  To change your master password, please confirm your current password below:",
                )

                if not continued:
                    mp = ""
                    while True:
                        addstr(stdscr, 12, 0, "> " + "*" * len(mp), reset=True)
                        move(stdscr, 12, 2 + len(mp))
                        stdscr.refresh()

                        ch = getch(stdscr)
                        if ch == curses.KEY_RESIZE:
                            continue

                        if ch in (curses.KEY_ENTER, 10, 13):
                            reset_footer(stdscr)

                            if mp == master_password:
                                new_password = choose_master_password(
                                    stdscr, username, master_password_only=True
                                )
                                if new_password is None:
                                    break

                                stdscr.clear()
                                continued = curses.KEY_ENTER
                                break
                            else:
                                addstr(
                                    stdscr,
                                    14,
                                    0,
                                    "  Incorrect password. Master password not changed.",
                                    curses.color_pair(3),
                                    reset=True,
                                )
                                addstr(stdscr, 15, 0, "  Press any key to go back...", reset=True)
                                getch(stdscr)
                                stdscr.clear()
                                break

                        elif ch == 27:  #* ESC key
                            stdscr.clear()
                            break

                        elif ch in (curses.KEY_BACKSPACE, 127, 8):
                            mp = mp[:-1]

                        elif (
                            (32 <= ch <= 126)
                            and (ch not in [92, 39, 34])
                            and len(mp) < 64
                        ):
                            mp += chr(ch)

                else:
                    continued = None

                    #* Changing master password
                    change_master_password(username, master_password, new_password)

                    reset_line(stdscr, 10, 0)
                    addstr(
                        stdscr,
                        10,
                        0,
                        "  Pending master password change...",
                        curses.color_pair(2),
                    )
                    addstr(
                        stdscr,
                        12,
                        0,
                        "  To apply, please restart the application.",
                        curses.A_BOLD,
                        reset=True,
                    )
                    addstr(stdscr, 13, 0, "  Press any key to exit...", reset=True)
                    getch(stdscr)

                    curses.endwin()
                    exit()

            elif current_pos == 3:
                addstr(stdscr, 12, 2, "Warning:", curses.color_pair(3) | curses.A_BOLD)
                addstr(
                    stdscr,
                    13,
                    2,
                    "You are about to delete your account. This action is ",
                    curses.color_pair(3),
                )
                addstr(
                    stdscr,
                    13,
                    55,
                    "irreversible",
                    curses.color_pair(3) | curses.A_UNDERLINE,
                )
                addstr(stdscr, 13, 67, "!", curses.color_pair(3))
                addstr(
                    stdscr,
                    14,
                    2,
                    "ALL stored passwords and data will be permanently lost.",
                    curses.color_pair(3),
                )
                addstr(
                    stdscr, 16, 2, "To confirm, please type your master password below."
                )
                footer(
                    stdscr,
                    "Press [ESC] to go back, and [Enter] to continue.",
                    attr=curses.A_UNDERLINE,
                )

                mp = ""
                while True:
                    addstr(stdscr, 18, 0, "> " + "*" * len(mp), reset=True)
                    move(stdscr, 18, 2 + len(mp))
                    stdscr.refresh()

                    ch = getch(stdscr)
                    if ch == curses.KEY_RESIZE:
                        continue

                    if ch in (curses.KEY_ENTER, 10, 13):
                        reset_footer(stdscr)

                        if mp == master_password:
                            #* Deleting account

                            from core.sqlutils import delete_user

                            delete_user(username)

                            addstr(
                                stdscr,
                                18,
                                0,
                                "  Account deleted successfully.",
                                curses.color_pair(2) | curses.A_BOLD,
                                reset=True,
                            )
                            addstr(stdscr, 19, 0, "  Press any key to continue...", reset=True)
                            getch(stdscr)

                            from core.utils import accounts_exist
                            from ui.launch.normal_launch import normal_launch
                            from ui.launch.first_time_launch import first_time_launch

                            if accounts_exist():
                                normal_launch(stdscr, "Welcome back, ")
                            else:
                                first_time_launch(stdscr)
                                normal_launch(stdscr, "Welcome, ")
                        else:
                            addstr(
                                stdscr,
                                16,
                                0,
                                "  Incorrect password. Account not deleted.",
                                curses.color_pair(3),
                                reset=True,
                            )
                            addstr(stdscr, 17, 0, "  Press any key to go back...", reset=True)
                            getch(stdscr)
                            stdscr.clear()
                            break

                    elif ch == 27:  #* ESC key
                        stdscr.clear()
                        break

                    elif ch in (curses.KEY_BACKSPACE, 127, 8):
                        mp = mp[:-1]

                    elif (
                        (32 <= ch <= 126) and (ch not in [92, 39, 34]) and len(mp) < 64
                    ):
                        mp += chr(ch)

        elif ch == 27:  #* ESC key
            stdscr.clear()
            break
