
#* For handling the master password

import curses


def create_master_password(stdscr):
    password = ""
    stdscr.addstr("Create master password:\n", curses.A_BOLD)
    requirements = {"len": False, "upperlower": False, "digit": False, "special": False}
    show_password = False

    while True:
        stdscr.move(1, 0)  #* Move cursor to requirements line
        stdscr.addstr("Requirements:\n")
        allow_typing = True

        #* Check if password meets length requirement
        stdscr.move(2, 0)
        if 12 <= len(password) <= 64:
            stdscr.addstr(
                "[\u2713] Requires at least 12 characters\n", curses.color_pair(2)
            )
            requirements["len"] = True
        elif len(password) > 64:
            stdscr.addstr(
                "[!] Cannot be greater than 64 characters\n", curses.color_pair(3)
            )
            requirements["len"] = False
            allow_typing = False  #! Prevents user from typing more than 64 characters
        else:
            stdscr.addstr("[X] Requires at least 12 characters\n", curses.color_pair(1))
            requirements["len"] = False

        #* Check if password has at least one uppercase and lowercase letter
        stdscr.move(3, 0)
        if any(c.isupper() for c in password) and any(c.islower() for c in password):
            stdscr.addstr(
                "[\u2713] Requires at least one uppercase and one lowercase letter\n",
                curses.color_pair(2),
            )
            requirements["upperlower"] = True
        else:
            stdscr.addstr(
                "[X] Requires at least one uppercase and one lowercase letter\n",
                curses.color_pair(1),
            )
            requirements["upperlower"] = False

        #* Check if password has at least one digit
        stdscr.move(4, 0)
        if any(c.isdigit() for c in password):
            stdscr.addstr(
                "[\u2713] Requires at least one numerical digit\n", curses.color_pair(2)
            )
            requirements["digit"] = True
        else:
            stdscr.addstr(
                "[X] Requires at least one numerical digit\n", curses.color_pair(1)
            )
            requirements["digit"] = False

        #* Check if password has at least one special character
        stdscr.move(5, 0)
        if any(c in "!#$%&()*+,-./:;<=>?@[]^_`{|}~" for c in password):
            stdscr.addstr(
                "[\u2713] Requires at least one special character\n",
                curses.color_pair(2),
            )
            requirements["special"] = True
        else:
            stdscr.addstr(
                "[X] Requires at least one special character\n", curses.color_pair(1)
            )
            requirements["special"] = False

        stdscr.move(6, 0)
        stdscr.clrtoeol()  #* Adds a new line

        stdscr.move(7, 0)
        if show_password:
            stdscr.addstr("Press 'Tab' to hide password\n")
            stdscr.addstr(8, 0, "Password: " + password + " ")
        else:
            stdscr.addstr("Press 'Tab' to show password\n")
            stdscr.addstr(8, 0, "Password: " + "*" * len(password) + " ")
        stdscr.move(8, 10 + len(password))  #* Move cursor to end of password
        stdscr.refresh()

        ch = stdscr.getch()  #* Get user key press

        #* If Enter is pressed and requirement is met, exit loop
        if ch in (curses.KEY_ENTER, 10, 13):
            if all(requirements.values()):
                break

        #* Toggle show/hide password on Alt key press
        elif ch == 9:
            show_password = not show_password

        #* Handle backspace
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            password = password[:-1]

        #* Accepts printable ASCII characters, except for [\, ", '], so long as the user is allowed to type
        elif (32 <= ch <= 126) and (ch not in [92, 39, 34]) and allow_typing:
            password += chr(ch)

    stdscr.clear()
    stdscr.move(0, 0)
    stdscr.refresh()
    stdscr.addstr("Password set successfully!\n", curses.A_BOLD)
    stdscr.getch()
