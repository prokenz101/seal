import curses
from csv import writer
from pickle import dump
from hashlib import sha256
from os import makedirs, urandom
from core.cutils import addstr, getch, move, reset_line


def choose_master_password(stdscr, username: str):
    """Prompt the user to create a master password."""

    #! Clear the terminal
    stdscr.clear()

    master_password = ""
    requirements = {"len": False, "upperlower": False, "digit": False, "special": False}
    show_password = False

    while True:
        addstr(stdscr, 0, 0, "Create master password", curses.A_BOLD)
        addstr(stdscr, 1, 0, "Requirements:")
        allow_typing = True

        #* Check if password meets length requirement
        if 12 <= len(master_password) <= 64:
            reset_line(stdscr, 2, 0)
            addstr(
                stdscr,
                2,
                0,
                "[\u2713] Requires at least 12 characters",
                curses.color_pair(2),
            )
            requirements["len"] = True
        elif len(master_password) > 64:
            addstr(
                stdscr,
                2,
                0,
                "[!] Cannot be greater than 64 characters",
                curses.color_pair(3),
            )
            requirements["len"] = False
            allow_typing = False  #! Prevents user from typing more than 64 characters
        else:
            addstr(
                stdscr,
                2,
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
                3,
                0,
                "[\u2713] Requires at least one uppercase and one lowercase letter",
                curses.color_pair(2),
            )
            requirements["upperlower"] = True
        else:
            addstr(
                stdscr,
                3,
                0,
                "[X] Requires at least one uppercase and one lowercase letter",
                curses.color_pair(1),
            )
            requirements["upperlower"] = False

        #* Check if password has at least one digit
        if any(c.isdigit() for c in master_password):
            addstr(
                stdscr,
                4,
                0,
                "[\u2713] Requires at least one numerical digit",
                curses.color_pair(2),
            )
            requirements["digit"] = True
        else:
            addstr(
                stdscr,
                4,
                0,
                "[X] Requires at least one numerical digit",
                curses.color_pair(1),
            )
            requirements["digit"] = False

        #* Check if password has at least one special character
        if any(c in "!#$%&()*+,-./:;<=>?@[]^_`{|}~" for c in master_password):
            addstr(
                stdscr,
                5,
                0,
                "[\u2713] Requires at least one special character",
                curses.color_pair(2),
            )
            requirements["special"] = True
        else:
            addstr(
                stdscr,
                5,
                0,
                "[X] Requires at least one special character",
                curses.color_pair(1),
            )
            requirements["special"] = False

        move(stdscr, 6, 0)
        stdscr.clrtoeol()  #* Adds a new line

        if show_password:
            addstr(stdscr, 7, 0, "Press [F2] to hide password", curses.color_pair(6))
            addstr(stdscr, 8, 0, "Password: " + master_password + " ")
        else:
            addstr(stdscr, 7, 0, "Press [F2] to show password", curses.color_pair(6))
            addstr(stdscr, 8, 0, f"Password: {'*' * len(master_password)} ")
        move(stdscr, 8, 10 + len(master_password))  #* Move cursor to end of password
        stdscr.refresh()

        ch = getch(stdscr)  #* Get user key press
        if ch == curses.KEY_RESIZE:
            continue

        #* If Enter is pressed and requirement is met, exit loop
        if ch in (curses.KEY_ENTER, 10, 13):
            if all(requirements.values()):
                #* Confirm password segment

                reset_line(stdscr, 7, 0)
                addstr(stdscr, 7, 0, "Password hidden", curses.color_pair(6))
                reset_line(stdscr, 8, 0)
                addstr(stdscr, 8, 0, f"Password: {'*' * len(master_password)} ")

                confirm_password = ""
                while True:
                    addstr(
                        stdscr,
                        10,
                        0,
                        f"Confirm password: {'*' * len(confirm_password)} ",
                    )
                    move(
                        stdscr, 10, 18 + len(confirm_password)
                    )  #* Move cursor to end of confirm password
                    stdscr.refresh()
                    confirm_ch = getch(stdscr)  #* Get user key press for confirm password
                    if confirm_ch == curses.KEY_RESIZE:
                        continue

                    #* Handle backspace
                    if confirm_ch in (curses.KEY_BACKSPACE, 127, 8):
                        confirm_password = confirm_password[:-1]

                    elif confirm_ch in (curses.KEY_ENTER, 10, 13):
                        if confirm_password == master_password:
                            break
                        else:
                            addstr(
                                stdscr,
                                11,
                                0,
                                "Passwords do not match! Try again.",
                                curses.color_pair(1),
                            )
                            reset_line(stdscr, 10, 0)
                            confirm_password = ""

                    #* Accepts printable ASCII characters, except for [\, ", '], so long as the user is allowed to type
                    elif (32 <= confirm_ch <= 126) and (confirm_ch not in [92, 39, 34]):
                        confirm_password += chr(confirm_ch)

                break

        #* Toggle show/hide password on F2 key press
        elif ch == curses.KEY_F2:
            show_password = not show_password

        #* Handle backspace
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            master_password = master_password[:-1]

        #* Accepts printable ASCII characters, except for [\, ", '], so long as the user is allowed to type
        elif (32 <= ch <= 126) and (ch not in [92, 39, 34]) and allow_typing:
            master_password += chr(ch)

    create_salt(username)

    reset_line(stdscr, 11, 0)
    reset_line(stdscr, 12, 0)
    addstr(
        stdscr,
        12,
        0,
        "[\u2713] Password set successfully!",
        curses.color_pair(2),
    )
    addstr(stdscr, 13, 0, "Press any key to continue...")
    getch(stdscr)

    with open("data/appdata/seal_core.csv", "a", newline="") as f:
        w = writer(f)
        username_hash = sha256(username.encode()).hexdigest()
        password_hash = sha256(master_password.encode()).hexdigest()
        w.writerow([username_hash, password_hash])

    stdscr.clear()
    stdscr.refresh()
    reset_line(stdscr, 1, 0)
    addstr(
        stdscr,
        1,
        0,
        "[\u2713] Account registered successfully!",
        curses.color_pair(2),
    )
    addstr(stdscr, 3, 0, "You may now log in.")
    addstr(stdscr, 4, 0, "Press any key to continue...")
    getch(stdscr)


def create_salt(username: str) -> None:
    """Create a salt file for the given username."""

    username_hash = sha256(username.encode()).hexdigest()
    salt = urandom(16)  #* Generate a random 16-byte salt
    makedirs("data/salts", exist_ok=True)

    with open(f"data/salts/{username_hash}_salt.dat", "wb") as f:
        dump(salt, f)
