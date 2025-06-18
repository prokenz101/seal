def choose_username(stdscr: curses.window) -> tuple[str, str]:
    #! Clear the terminal
    stdscr.clear()

    username = ""
    stdscr.addstr("Create username:\n", curses.A_BOLD)
    requirements = {"length": False, "alphanumeric_lowercase": False}

    while True:
        stdscr.move(1, 0)  #* Move cursor to requirements line
        stdscr.addstr("Requirements:\n")
        allow_typing = True

        #* Check if username meets length requirement
        stdscr.move(2, 0)
        if len(username) < 3:
            stdscr.addstr("[X] Requires at least 3 characters\n", curses.color_pair(1))
            requirements["length"] = False
        elif len(username) > 16:
            stdscr.addstr(
                "[!] Cannot be greater than 16 characters\n", curses.color_pair(3)
            )
            requirements["length"] = False
            allow_typing = False
        else:
            stdscr.addstr(
                "[\u2713] Requires at least 3 characters\n", curses.color_pair(2)
            )
            requirements["length"] = True

        #* Check if username contains only lowercase letters and numbers
        stdscr.move(3, 0)
        if not all(c.islower() or c.isdigit() for c in username):
            stdscr.addstr(
                "[!] Only lowercase letters and numbers are allowed\n",
                curses.color_pair(3),
            )
            allow_typing = False
            requirements["alphanumeric_lowercase"] = False
        else:
            stdscr.addstr(
                "[-] Only lowercase letters and numbers are allowed\n",
                curses.color_pair(4),
            )
            requirements["alphanumeric_lowercase"] = True

        stdscr.move(4, 0)
        stdscr.clrtoeol()  #* Adds a new line

        stdscr.addstr(5, 0, "Username: " + username + " ")

        stdscr.move(5, 10 + len(username))  #* Move cursor to end of username
        stdscr.refresh()

        ch = stdscr.getch()  #* Get user key press

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
    stdscr.move(0, 0)
    stdscr.refresh()
    stdscr.addstr("Username set successfully!\n", curses.A_BOLD)
    stdscr.getch()
    return choose_master_password(stdscr, username)

