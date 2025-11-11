import curses
from core.sqlutils import username_exists
from ui.master_password import choose_master_password
from core.cutils import addstr, getch, move, reset_line


def choose_username(stdscr):
    """Prompt the user to create a username."""

    #! Clear the terminal
    stdscr.clear()

    username = ""
    requirements = {"length": False, "alphanumeric_lowercase": False}

    while True:
        addstr(stdscr, 0, 0, "Create username", curses.A_BOLD)
        addstr(stdscr, 1, 0, "Requirements:")
        allow_typing = True

        #* Check if username meets length requirement
        if len(username) < 3:
            addstr(
                stdscr,
                2,
                0,
                "[X] Requires at least 3 characters",
                curses.color_pair(1),
            )
            requirements["length"] = False
        elif len(username) > 16:
            addstr(
                stdscr,
                2,
                0,
                "[!] Cannot be greater than 16 characters",
                curses.color_pair(3),
            )
            requirements["length"] = False
            allow_typing = False
        else:
            reset_line(stdscr, 2, 0)
            addstr(
                stdscr,
                2,
                0,
                "[\u2713] Requires at least 3 characters",
                curses.color_pair(2),
            )
            requirements["length"] = True

        #* Check if username contains only lowercase letters and numbers
        if not all(c.islower() or c.isdigit() for c in username):
            addstr(
                stdscr,
                3,
                0,
                "[!] Only lowercase letters and numbers are allowed",
                curses.color_pair(3),
            )
            allow_typing = False
            requirements["alphanumeric_lowercase"] = False
        else:
            addstr(
                stdscr,
                3,
                0,
                "[-] Only lowercase letters and numbers are allowed",
                curses.color_pair(4),
            )
            requirements["alphanumeric_lowercase"] = True

        move(stdscr, 4, 0)
        stdscr.clrtoeol()  #* Adds a new line

        addstr(stdscr, 5, 0, "Username: " + username + " ")

        move(stdscr, 5, 10 + len(username))  #* Move cursor to end of username
        stdscr.refresh()

        ch = getch(stdscr)  #* Get user key press
        if ch == curses.KEY_RESIZE:
            continue

        #* If Enter is pressed and requirement is met, exit loop
        if ch in (curses.KEY_ENTER, 10, 13):
            if all(requirements.values()):
                break

        #* Handle backspace
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            username = username[:-1]

        #* Accepts only numbers and lowercase letters, so long as the user is allowed to type
        elif (32 <= ch <= 126) and allow_typing:
            username += chr(ch)

    # TODO: Add username to file or database

    reset_line(stdscr, 7, 0)
    addstr(
        stdscr,
        7,
        0,
        "[\u2713] Username set successfully!",
        curses.color_pair(2),
    )
    addstr(stdscr, 8, 0, "Press any key to continue...")
    getch(stdscr)
    choose_master_password(stdscr, username)
