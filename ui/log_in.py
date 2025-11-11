import curses
from core.cutils import addstr, getch, move, reset_line, footer
from core.sqlutils import account_exists
from ui.main_menu import main_menu


def log_in(stdscr, welcome):
    """Handle the login process for the user."""

    #! Clear the terminal
    stdscr.clear()
    username = ""
    password = ""
    show_password = False
    movements = [[2, 10], [5, 10]]
    current_pos = 0
    pos_to_data = {0: "username", 1: "password"}

    with open("data/appdata/seal_core.csv", "r") as f:
        r = list(reader(f))

    while True:
        addstr(stdscr, 0, 0, "Log in", curses.A_BOLD)
        move(stdscr, 1, 0)
        stdscr.clrtoeol()
        footer(
            stdscr,
            "Use [▲] and [▼] arrow keys to navigate, and [Enter] to confirm.",
        )

        addstr(stdscr, 2, 0, f"Username: {username}")
        move(stdscr, 3, 0)
        stdscr.clrtoeol()

        if show_password:
            addstr(stdscr, 4, 0, "Press [F2] to hide password", curses.color_pair(6))
            addstr(stdscr, 5, 0, f"Password: {password}")
        else:
            addstr(stdscr, 4, 0, "Press [F2] to show password", curses.color_pair(6))
            addstr(stdscr, 5, 0, f"Password: {'*' * len(password)}")

        move(stdscr, *movements[current_pos])
        ch = getch(stdscr)
        if ch == curses.KEY_RESIZE:
            continue

        if ch == curses.KEY_F2:  #* F2 key
            show_password = not show_password

        elif ch == curses.KEY_UP:
            if current_pos > 0:
                current_pos -= 1
                reset_line(stdscr, movements[current_pos + 1][0], 0)
                reset_line(stdscr, movements[current_pos][0], 0)

        elif ch == curses.KEY_DOWN or ch == 9:
            if current_pos < 1:
                current_pos += 1
                reset_line(stdscr, movements[current_pos - 1][0], 0)
                reset_line(stdscr, movements[current_pos][0], 0)

        elif ch in (curses.KEY_ENTER, 10, 13):
            msg = None
            if username == "" and password == "":
                msg = "Please type a valid username and password."
            elif username == "":
                msg = "Please type a valid username."
            elif password == "":
                msg = "Please type a valid password."

            if msg:
                reset_line(stdscr, 7, 0)
                addstr(stdscr, 7, 0, msg, curses.color_pair(3))
                continue

            skip = True
            username_hash = sha256(username.encode()).hexdigest()
            password_hash = sha256(password.encode()).hexdigest()

            for row in r:
                if skip:
                    skip = False  #* Skip the SQL row
                    continue

                if row[0] == username_hash and row[1] == password_hash:
                    #* Successful login
                    reset_line(stdscr, 7, 0)
                    addstr(
                        stdscr,
                        7,
                        0,
                        welcome + username,
                        curses.color_pair(2),
                    )
                    addstr(stdscr, 8, 0, "Press any key to continue...")
                    getch(stdscr)
                    break
            else:
                #* Failed login
                reset_line(stdscr, 7, 0)
                addstr(
                    stdscr, 7, 0, "Invalid username or password.", curses.color_pair(3)
                )
                continue

            break

        else:
            #* Edit mode
            editing = pos_to_data[current_pos]
            if editing == "username":
                if 32 <= ch <= 126:  #* Printable ASCII characters
                    username += chr(ch)
                    movements[current_pos][1] += 1
                elif ch in (curses.KEY_BACKSPACE, 127, 8):
                    if username:
                        username = username[:-1]
                        movements[current_pos][1] -= 1

            elif editing == "password":
                if (32 <= ch <= 126) and (ch not in [92, 39, 34]):
                    password += chr(ch)
                    movements[current_pos][1] += 1
                elif ch in (curses.KEY_BACKSPACE, 127, 8):
                    if password:
                        password = password[:-1]
                        movements[current_pos][1] -= 1

            reset_line(stdscr, movements[current_pos][0], 0)

    #* Enter vault
    # TODO: Remove this clear when enter vault is implemented
    stdscr.clear()
