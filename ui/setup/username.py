import curses
from core.sqlutils import username_exists
from ui.setup.master_password import choose_master_password
from core.cutils import addstr, footer, getch, move, reset_footer, reset_line


def choose_username(stdscr, username_only=False):
    """Prompt the user to create a username."""

    #! Clear the terminal
    stdscr.clear()

    username = ""
    requirements = {"length": False, "alphanumeric_lowercase": False}

    header = "Create username:"
    if username_only:
        header = "Edit username:"

    while True:
        addstr(stdscr, 0, 0, "seal", curses.color_pair(4) | curses.A_BOLD)
        addstr(stdscr, 0, 4, f" — {header.title()[:-1]}", curses.A_BOLD)
        addstr(stdscr, 2, 0, f"{header}", curses.A_BOLD)
        footer(stdscr, "Press [ESC] to go back.")
        addstr(stdscr, 3, 0, "Requirements:")
        allow_typing = True

        #* Check if username meets length requirement
        if len(username) < 3:
            addstr(
                stdscr,
                4,
                0,
                "[X] Requires at least 3 characters",
                curses.color_pair(1),
            )
            requirements["length"] = False
        elif len(username) > 16:
            addstr(
                stdscr,
                4,
                0,
                "[!] Cannot be greater than 16 characters",
                curses.color_pair(3),
            )
            requirements["length"] = False
            allow_typing = False
        else:
            addstr(
                stdscr,
                4,
                0,
                "[\u2713] Requires at least 3 characters",
                curses.color_pair(2),
                reset=True,
            )
            requirements["length"] = True

        #* Check if username contains only lowercase letters and numbers
        if not all(c.islower() or c.isdigit() for c in username):
            addstr(
                stdscr,
                5,
                0,
                "[!] Only lowercase letters and numbers are allowed",
                curses.color_pair(3),
            )
            allow_typing = False
            requirements["alphanumeric_lowercase"] = False
        else:
            addstr(
                stdscr,
                5,
                0,
                "[-] Only lowercase letters and numbers are allowed",
                curses.color_pair(4),
            )
            requirements["alphanumeric_lowercase"] = True

        addstr(stdscr, 7, 0, "Username: " + username + " ")

        move(stdscr, 7, 10 + len(username))  #* Move cursor to end of username
        stdscr.refresh()

        ch = getch(stdscr)  #* Get user key press
        if ch == curses.KEY_RESIZE:
            continue

        #* If Enter is pressed and requirement is met, exit loop
        if ch in (curses.KEY_ENTER, 10, 13):
            if all(requirements.values()):
                if username_exists(username):
                    addstr(
                        stdscr,
                        8,
                        0,
                        "This username is already in use.",
                        curses.color_pair(1),
                    )
                else:
                    if username_only:
                        return username

                    reset_line(stdscr, 8, 0)
                    addstr(
                        stdscr,
                        9,
                        0,
                        "[\u2713] Username set successfully!",
                        curses.color_pair(2),
                        reset=True,
                    )
                    addstr(stdscr, 10, 0, "Press any key to continue...")
                    reset_footer(stdscr)
                    getch(stdscr)
                    choose_master_password(stdscr, username)

            else:
                addstr(
                    stdscr,
                    9,
                    0,
                    "Username does not meet all requirements.",
                    curses.color_pair(3),
                )
                addstr(stdscr, 10, 0, "Press any key to continue...", reset=True)
                getch(stdscr)
                reset_line(stdscr, 9, 0)
                reset_line(stdscr, 10, 0)

        #* Handle backspace
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            username = username[:-1]

        #* Accepts only numbers and lowercase letters, so long as the user is allowed to type
        elif (32 <= ch <= 126) and allow_typing:
            username += chr(ch)

        elif ch == 27:  #* ESC key
            stdscr.clear()
            if username_only:
                return None

            break
