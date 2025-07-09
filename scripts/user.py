
#* For handling the master password

import curses
from scripts.curses_utils import getch, addstr, move, reset_line


def choose_username(stdscr) -> tuple[str, str]:
    #! Clear the terminal
    stdscr.clear()

    username = ""
    requirements = {"length": False, "alphanumeric_lowercase": False}

    while True:
        addstr(stdscr, 0, 0, "Create username:\n", curses.A_BOLD)
        addstr(stdscr, 1, 0, "Requirements:\n")
        allow_typing = True

        #* Check if username meets length requirement
        if len(username) < 3:
            addstr(
                stdscr,
                2,
                0,
                "[X] Requires at least 3 characters\n",
                curses.color_pair(1),
            )
            requirements["length"] = False
        elif len(username) > 16:
            addstr(
                stdscr,
                2,
                0,
                "[!] Cannot be greater than 16 characters\n",
                curses.color_pair(3),
            )
            requirements["length"] = False
            allow_typing = False
        else:
            addstr(
                stdscr,
                2,
                0,
                "[\u2713] Requires at least 3 characters\n",
                curses.color_pair(2),
            )
            requirements["length"] = True

        #* Check if username contains only lowercase letters and numbers
        if not all(c.islower() or c.isdigit() for c in username):
            addstr(
                stdscr,
                3,
                0,
                "[!] Only lowercase letters and numbers are allowed\n",
                curses.color_pair(3),
            )
            allow_typing = False
            requirements["alphanumeric_lowercase"] = False
        else:
            addstr(
                stdscr,
                3,
                0,
                "[-] Only lowercase letters and numbers are allowed\n",
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

    stdscr.clear()
    stdscr.refresh()
    addstr(stdscr, 0, 0, "Username set successfully!\n", curses.A_BOLD)
    getch(stdscr)
    return choose_master_password(stdscr, username)


def choose_master_password(stdscr, username: str) -> tuple[str, str]:
    #! Clear the terminal
    stdscr.clear()

    master_password = ""
    requirements = {"len": False, "upperlower": False, "digit": False, "special": False}
    show_password = False

    while True:
        addstr(stdscr, 0, 0, "Create master password:\n", curses.A_BOLD)
        addstr(stdscr, 1, 0, "Requirements:\n")
        allow_typing = True

        #* Check if password meets length requirement
        if 12 <= len(master_password) <= 64:
            addstr(
                stdscr,
                2,
                0,
                "[\u2713] Requires at least 12 characters\n",
                curses.color_pair(2),
            )
            requirements["len"] = True
        elif len(master_password) > 64:
            addstr(
                stdscr,
                2,
                0,
                "[!] Cannot be greater than 64 characters\n",
                curses.color_pair(3),
            )
            requirements["len"] = False
            allow_typing = False  #! Prevents user from typing more than 64 characters
        else:
            addstr(
                stdscr,
                2,
                0,
                "[X] Requires at least 12 characters\n",
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
                "[\u2713] Requires at least one uppercase and one lowercase letter\n",
                curses.color_pair(2),
            )
            requirements["upperlower"] = True
        else:
            addstr(
                stdscr,
                3,
                0,
                "[X] Requires at least one uppercase and one lowercase letter\n",
                curses.color_pair(1),
            )
            requirements["upperlower"] = False

        #* Check if password has at least one digit
        if any(c.isdigit() for c in master_password):
            addstr(
                stdscr,
                4,
                0,
                "[\u2713] Requires at least one numerical digit\n",
                curses.color_pair(2),
            )
            requirements["digit"] = True
        else:
            addstr(
                stdscr,
                4,
                0,
                "[X] Requires at least one numerical digit\n",
                curses.color_pair(1),
            )
            requirements["digit"] = False

        #* Check if password has at least one special character
        if any(c in "!#$%&()*+,-./:;<=>?@[]^_`{|}~" for c in master_password):
            addstr(
                stdscr,
                5,
                0,
                "[\u2713] Requires at least one special character\n",
                curses.color_pair(2),
            )
            requirements["special"] = True
        else:
            addstr(
                stdscr,
                5,
                0,
                "[X] Requires at least one special character\n",
                curses.color_pair(1),
            )
            requirements["special"] = False

        move(stdscr, 6, 0)
        stdscr.clrtoeol()  #* Adds a new line

        if show_password:
            addstr(stdscr, 7, 0, "Press 'Tab' to hide password")
            addstr(stdscr, 8, 0, "Password: " + master_password + " ")
        else:
            addstr(stdscr, 7, 0, "Press 'Tab' to show password")
            addstr(stdscr, 8, 0, "Password: " + "*" * len(master_password) + " ")
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
                addstr(stdscr, 8, 0, "Password: " + "*" * len(master_password) + " ")

                confirm_password = ""
                while True:
                    addstr(stdscr, 10, 0, "Confirm password: " + "*" * len(confirm_password) + " ")
                    move(stdscr, 10, 18 + len(confirm_password))  #* Move cursor to end of confirm password
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
                            addstr(stdscr, 11, 0, "Passwords do not match! Try again.\n", curses.color_pair(1))
                            reset_line(stdscr, 10, 0)
                            confirm_password = ""

                    #* Accepts printable ASCII characters, except for [\, ", '], so long as the user is allowed to type
                    elif (32 <= confirm_ch <= 126) and (confirm_ch not in [92, 39, 34]):
                        confirm_password += chr(confirm_ch)

                break
        #* Toggle show/hide password on Tab key press
        elif ch == 9:
            show_password = not show_password

        #* Handle backspace
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            master_password = master_password[:-1]

        #* Accepts printable ASCII characters, except for [\, ", '], so long as the user is allowed to type
        elif (32 <= ch <= 126) and (ch not in [92, 39, 34]) and allow_typing:
            master_password += chr(ch)

    create_salt(username)

    stdscr.clear()
    stdscr.refresh()
    addstr(stdscr, 0, 0, "Password set successfully!\n", curses.A_BOLD)
    getch(stdscr)

    return username, master_password


def create_salt(username: str) -> None:
    from pickle import dump
    from hashlib import sha256
    from os import urandom, makedirs

    username_hash = sha256(username.encode()).hexdigest()
    salt = urandom(16)
    makedirs("salts", exist_ok=True)

    with open(f"salts/{username_hash}_salt.dat", "wb") as f:
        dump(salt, f)
