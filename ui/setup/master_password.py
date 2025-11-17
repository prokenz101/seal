import curses
from time import sleep
from core.utils import create_salt
from core.cutils import (
    addstr,
    footer,
    getch,
    move,
    reset_footer,
    reset_line,
    reset_lines,
)


def choose_master_password(stdscr, username: str, master_password_only=False):
    """Prompt the user to create a master password."""

    #! Clear the terminal
    stdscr.clear()

    master_password = ""
    requirements = {"len": False, "upperlower": False, "digit": False, "special": False}
    show_password = False
    registered = False

    while True:
        addstr(stdscr, 0, 0, "seal", curses.color_pair(4) | curses.A_BOLD)
        addstr(
            stdscr,
            0,
            4,
            f" — {'Set' if not master_password_only else 'Edit'} Master Password",
            curses.A_BOLD,
        )
        addstr(
            stdscr,
            2,
            0,
            f"{'Create' if not master_password_only else 'Edit'} master password:",
            curses.A_BOLD,
        )
        footer(stdscr, "Press [ESC] to go back.")
        addstr(stdscr, 3, 0, "Requirements:")
        allow_typing = True

        #* Check if password meets length requirement
        if 12 <= len(master_password) <= 64:
            addstr(
                stdscr,
                4,
                0,
                "[\u2713] Requires at least 12 characters",
                curses.color_pair(2),
                reset=True,
            )
            requirements["len"] = True
        elif len(master_password) > 64:
            addstr(
                stdscr,
                4,
                0,
                "[!] Cannot be greater than 64 characters",
                curses.color_pair(3),
            )
            requirements["len"] = False
            allow_typing = False  #! Prevents user from typing more than 64 characters
        else:
            addstr(
                stdscr,
                4,
                0,
                "[X] Requires at least 12 characters",
                curses.color_pair(1),
            )
            requirements["len"] = False

        #* Check if password has at least one uppercase and lowercase letter
        if any(c.isupper() for c in master_password) and any(
            c.islower() for c in master_password
        ):
            addstr(
                stdscr,
                5,
                0,
                "[\u2713] Requires at least one uppercase and one lowercase letter",
                curses.color_pair(2),
            )
            requirements["upperlower"] = True
        else:
            addstr(
                stdscr,
                5,
                0,
                "[X] Requires at least one uppercase and one lowercase letter",
                curses.color_pair(1),
            )
            requirements["upperlower"] = False

        #* Check if password has at least one digit
        if any(c.isdigit() for c in master_password):
            addstr(
                stdscr,
                6,
                0,
                "[\u2713] Requires at least one numerical digit",
                curses.color_pair(2),
            )
            requirements["digit"] = True
        else:
            addstr(
                stdscr,
                6,
                0,
                "[X] Requires at least one numerical digit",
                curses.color_pair(1),
            )
            requirements["digit"] = False

        #* Check if password has at least one special character
        if any(c in "!#$%&()*+,-./:;<=>?@[]^_`{|}~" for c in master_password):
            addstr(
                stdscr,
                7,
                0,
                "[\u2713] Requires at least one special character",
                curses.color_pair(2),
            )
            requirements["special"] = True
        else:
            addstr(
                stdscr,
                7,
                0,
                "[X] Requires at least one special character",
                curses.color_pair(1),
            )
            requirements["special"] = False

        if show_password:
            addstr(stdscr, 9, 0, "Press [F2] to hide password", curses.color_pair(6))
            addstr(stdscr, 10, 0, "Password: " + master_password + " ")
        else:
            addstr(stdscr, 9, 0, "Press [F2] to show password", curses.color_pair(6))
            addstr(stdscr, 10, 0, f"Password: {'*' * len(master_password)} ")
        move(stdscr, 10, 10 + len(master_password))  #* Move cursor to end of password
        stdscr.refresh()

        ch = getch(stdscr)  #* Get user key press
        if ch == curses.KEY_RESIZE:
            continue

        #* If Enter is pressed and requirement is met, exit loop
        if ch in (curses.KEY_ENTER, 10, 13):
            if all(requirements.values()):
                #* Confirm password segment

                addstr(
                    stdscr, 9, 0, "Password hidden", curses.color_pair(6), reset=True
                )
                addstr(
                    stdscr,
                    10,
                    0,
                    f"Password: {'*' * len(master_password)} ",
                    reset=True,
                )

                addstr(stdscr, 12, 0, "Warning:", curses.color_pair(3) | curses.A_BOLD)
                addstr(
                    stdscr,
                    13,
                    0,
                    "The master password cannot be recovered if lost.",
                    curses.A_BOLD,
                )
                addstr(stdscr, 13, 20, "cannot", curses.A_BOLD | curses.A_UNDERLINE)
                addstr(stdscr, 13, 26, " be recovered if lost.", curses.A_BOLD)
                addstr(
                    stdscr,
                    15,
                    0,
                    "Forgetting the master password will result in ",
                    curses.A_BOLD,
                )
                addstr(
                    stdscr, 15, 46, "permanent loss", curses.A_BOLD | curses.A_UNDERLINE
                )
                addstr(stdscr, 15, 60, " of", curses.A_BOLD)
                addstr(
                    stdscr,
                    16,
                    0,
                    "the account and all stored credentials.",
                    curses.A_BOLD,
                )
                addstr(
                    stdscr,
                    18,
                    0,
                    "Proceed only after making sure the master password is securely saved.",
                    curses.A_BOLD,
                )
                reset_footer(stdscr)
                stdscr.refresh()
                sleep(3)
                curses.flushinp()  #* Clear input buffer to avoid accidental key presses
                stdscr.addstr(
                    20, 0, "Press [ESC] to go back, or any other key to continue..."
                )
                warning_ch = getch(stdscr)
                if warning_ch == curses.KEY_RESIZE:
                    continue

                if warning_ch == 27:  #* ESC key
                    reset_lines(
                        stdscr,
                        (12, 0),
                        (13, 0),
                        (15, 0),
                        (16, 0),
                        (18, 0),
                        (20, 0),
                    )

                else:
                    confirm_password = ""
                    while True:
                        reset_line(stdscr, 20, 0)
                        addstr(
                            stdscr,
                            20,
                            0,
                            f"Confirm password: {'*' * len(confirm_password)} ",
                        )
                        move(
                            stdscr, 20, 18 + len(confirm_password)
                        )  #* Move cursor to end of confirm password
                        stdscr.refresh()
                        confirm_ch = getch(
                            stdscr
                        )  #* Get user key press for confirm password
                        if confirm_ch == curses.KEY_RESIZE:
                            continue

                        #* Handle backspace
                        if confirm_ch in (curses.KEY_BACKSPACE, 127, 8):
                            confirm_password = confirm_password[:-1]

                        elif confirm_ch in (curses.KEY_ENTER, 10, 13):
                            if confirm_password == master_password:
                                if master_password_only:
                                    return master_password

                                create_salt(username)

                                reset_line(stdscr, 22, 0)
                                addstr(
                                    stdscr,
                                    23,
                                    0,
                                    "[\u2713] Password set successfully!",
                                    curses.color_pair(2),
                                    reset=True,
                                )
                                addstr(stdscr, 24, 0, "Press any key to continue...")
                                reset_footer(stdscr)
                                getch(stdscr)

                                from core.sqlutils import add_user

                                add_user(username, master_password)

                                stdscr.clear()
                                stdscr.refresh()
                                addstr(
                                    stdscr,
                                    0,
                                    0,
                                    "seal",
                                    curses.color_pair(4) | curses.A_BOLD,
                                )
                                addstr(
                                    stdscr,
                                    2,
                                    0,
                                    "[\u2713] Account registered successfully!",
                                    curses.color_pair(2),
                                )
                                registered = True
                                addstr(stdscr, 4, 0, "You may now log in.")
                                addstr(stdscr, 5, 0, "Press any key to continue...")
                                getch(stdscr)

                                from ui.launch.normal_launch import normal_launch

                                normal_launch(stdscr, welcome=f"Welcome, ")
                                break
                            else:
                                addstr(
                                    stdscr,
                                    24,
                                    0,
                                    "Passwords do not match! Try again.",
                                    curses.color_pair(1),
                                )
                                reset_line(stdscr, 21, 0)
                                confirm_password = ""

                        #* Accepts printable ASCII characters, except for [\, ", '], so long as the user is allowed to type
                        elif (32 <= confirm_ch <= 126) and (
                            confirm_ch not in [92, 39, 34]
                        ):
                            confirm_password += chr(confirm_ch)

                        elif confirm_ch == 27:  #* ESC key
                            reset_lines(
                                stdscr,
                                (12, 0),
                                (13, 0),
                                (15, 0),
                                (16, 0),
                                (18, 0),
                                (20, 0),
                                (21, 0),
                                (22, 0)
                            )
                            break
            else:
                addstr(
                    stdscr,
                    12,
                    0,
                    "Password does not meet all requirements.",
                    curses.color_pair(3),
                )
                addstr(stdscr, 13, 0, "Press any key to continue...", reset=True)
                getch(stdscr)
                reset_line(stdscr, 12, 0)
                reset_line(stdscr, 13, 0)

        #* Toggle show/hide password on F2 key press
        elif ch == curses.KEY_F2:
            show_password = not show_password

        #* Handle backspace
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            master_password = master_password[:-1]

        #* Accepts printable ASCII characters, except for [\, ", '], so long as the user is allowed to type
        elif (32 <= ch <= 126) and (ch not in [92, 39, 34]) and allow_typing:
            master_password += chr(ch)

        elif ch == 27:  #* ESC key
            if not registered:
                stdscr.clear()

                if master_password_only:
                    return None
                break
