import curses
from scripts.curses_utils import reset_line, getch, move, addstr, footer


def first_time_launch(stdscr):
    #! Clear the terminal
    stdscr.clear()

    colors = [curses.color_pair(7) | curses.A_UNDERLINE, curses.color_pair(5)]
    curses.curs_set(0)

    while True:
        addstr(stdscr, 0, 11, "Welcome to", curses.A_BOLD)
        move(stdscr, 1, 0)
        stdscr.clrtoeol()
        addstr(stdscr, 2, 0, "███████╗███████╗ █████╗ ██╗     ", curses.color_pair(4))
        addstr(stdscr, 3, 0, "██╔════╝██╔════╝██╔══██╗██║     ", curses.color_pair(4))
        addstr(stdscr, 4, 0, "███████╗█████╗  ███████║██║     ", curses.color_pair(4))
        addstr(stdscr, 5, 0, "╚════██║██╔══╝  ██╔══██║██║     ", curses.color_pair(4))
        addstr(stdscr, 6, 0, "███████║███████╗██║  ██║███████╗", curses.color_pair(4))
        addstr(stdscr, 7, 0, "╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝", curses.color_pair(4))
        move(stdscr, 8, 0)
        stdscr.clrtoeol()
        addstr(stdscr, 9, 0, "Choose an option:")
        move(stdscr, 10, 0)
        stdscr.clrtoeol()
        addstr(stdscr, 11, 7, "Get Started", colors[0])
        addstr(stdscr, 11, 21, "Exit", colors[1])
        footer(
            stdscr, "Use [◀] and [▶] arrow keys to navigate, and [Enter] to confirm."
        )

        ch = getch(stdscr)  #* Wait for user key press
        if ch == curses.KEY_RESIZE:
            continue

        if ch == curses.KEY_RIGHT:
            colors = [curses.color_pair(5), curses.color_pair(7) | curses.A_UNDERLINE]
        elif ch == curses.KEY_LEFT:
            colors = [curses.color_pair(7) | curses.A_UNDERLINE, curses.color_pair(5)]

        #* If Enter is pressed and requirement is met, exit loop
        elif ch in (curses.KEY_ENTER, 10, 13):
            break

    stdscr.clear()
    curses.curs_set(1)
    move(stdscr, 0, 0)
    if colors[0] == curses.color_pair(7) | curses.A_UNDERLINE:
        setup_my_sql(stdscr)
        from scripts.user import choose_username

        choose_username(stdscr)
    else:
        #! Exiting...
        pass


def normal_launch(stdscr):
    #! Clear the terminal
    stdscr.clear()

    colors = [
        curses.color_pair(7) | curses.A_UNDERLINE,
        curses.color_pair(5),
        curses.color_pair(5),
    ]

    while True:
        move(stdscr, 0, 0)
        stdscr.clrtoeol()
        addstr(stdscr, 1, 0, "███████╗███████╗ █████╗ ██╗     ", curses.color_pair(4))
        addstr(stdscr, 2, 0, "██╔════╝██╔════╝██╔══██╗██║     ", curses.color_pair(4))
        addstr(stdscr, 3, 0, "███████╗█████╗  ███████║██║     ", curses.color_pair(4))
        addstr(stdscr, 4, 0, "╚════██║██╔══╝  ██╔══██║██║     ", curses.color_pair(4))
        addstr(stdscr, 5, 0, "███████║███████╗██║  ██║███████╗", curses.color_pair(4))
        addstr(stdscr, 6, 0, "╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝", curses.color_pair(4))
        move(stdscr, 7, 0)
        stdscr.clrtoeol()
        addstr(stdscr, 8, 0, "Choose an option:")
        move(stdscr, 9, 0)
        stdscr.clrtoeol()
        addstr(stdscr, 10, 2, "Log in", colors[0])
        addstr(stdscr, 10, 11, "MySQL Setup", colors[1])
        addstr(stdscr, 10, 25, "Exit", colors[2])
        footer(
            stdscr, "Use [◀] and [▶] arrow keys to navigate, and [Enter] to confirm."
        )

        ch = getch(stdscr)  #* Wait for user key press
        if ch == curses.KEY_RESIZE:
            continue

        if ch == curses.KEY_RIGHT:
            index = colors.index(curses.color_pair(7) | curses.A_UNDERLINE)
            if index < 2:
                colors[index] = curses.color_pair(5)
                colors[index + 1] = curses.color_pair(7) | curses.A_UNDERLINE
        elif ch == curses.KEY_LEFT:
            index = colors.index(curses.color_pair(7) | curses.A_UNDERLINE)
            if index > 0:
                colors[index] = curses.color_pair(5)
                colors[index - 1] = curses.color_pair(7) | curses.A_UNDERLINE

        #* If Enter is pressed and requirement is met, exit loop
        elif ch in (curses.KEY_ENTER, 10, 13):
            break

    stdscr.clear()
    curses.curs_set(1)
    move(stdscr, 0, 0)
    if colors[0] == curses.color_pair(7) | curses.A_UNDERLINE:
        log_in(stdscr)
    elif colors[1] == curses.color_pair(7) | curses.A_UNDERLINE:
        setup_my_sql(stdscr)
        normal_launch(stdscr)
    else:
        #! Exiting...
        pass


def setup_my_sql(stdscr):
    #! Clear the terminal
    stdscr.clear()

    data = {
        "host": "localhost (default)",
        "port": "3306 (default)",
        "username": "root (default)",
        "password": "",
    }

    colors = [curses.color_pair(6), curses.color_pair(6), curses.color_pair(6)]
    movements = [[5, 10], [4, 10], [3, 6], [2, 6]]
    current_pos = 0
    pos_to_data = {2: "host", 3: "port", 4: "username", 5: "password"}

    while True:
        addstr(stdscr, 0, 0, "Set up MySQL connection", curses.A_BOLD)
        move(stdscr, 1, 0)
        stdscr.clrtoeol()
        footer(
            stdscr,
            "Use [▲] and [▼] arrow keys to navigate, and [Enter] to confirm.",
        )
        addstr(stdscr, 2, 0, f"Host: {data['host']}", colors[0])
        addstr(stdscr, 3, 0, f"Port: {data['port']}", colors[1])
        addstr(stdscr, 4, 0, f"Username: {data['username']}", colors[2])
        addstr(stdscr, 5, 0, f"Password: {data['password']}", curses.A_BOLD)

        move(stdscr, *movements[current_pos])
        ch = getch(stdscr)
        if ch == curses.KEY_RESIZE:
            continue

        if ch == curses.KEY_UP and current_pos < 3:
            current_pos += 1
            editing = pos_to_data[movements[current_pos][0]]
            colors[3 - current_pos] = curses.color_pair(5)

            if " (default)" in data[editing]:
                data[editing] = ""

            if current_pos > 1:
                prompt = data[pos_to_data[movements[current_pos - 1][0]]]
                if prompt == "":
                    data[pos_to_data[movements[current_pos - 1][0]]] = (
                        "root (default)"
                        if editing == "port"
                        else "3306 (default)" if editing == "host" else ""
                    )
                    colors[4 - current_pos] = curses.color_pair(6)
                elif prompt == "3306" and editing == "host":
                    data[pos_to_data[movements[current_pos - 1][0]]] += " (default)"
                    colors[4 - current_pos] = curses.color_pair(6)
                    movements[2][1] = 6
                elif prompt == "root" and editing == "port":
                    data[pos_to_data[movements[current_pos - 1][0]]] += " (default)"
                    colors[4 - current_pos] = curses.color_pair(6)
                    movements[1][1] = 10
                else:
                    colors[4 - current_pos] = curses.color_pair(5) | curses.A_ITALIC

            reset_line(stdscr, movements[current_pos - 1][0], 0)
            reset_line(stdscr, movements[current_pos][0], 0)

        elif (ch == curses.KEY_DOWN or ch == 9) and current_pos > 0:
            current_pos -= 1
            editing = pos_to_data[movements[current_pos][0]]
            if current_pos > 0:
                colors[3 - current_pos] = curses.color_pair(5)

            if " (default)" in data[editing]:
                data[editing] = ""

            if current_pos < 3:
                prompt = data[pos_to_data[movements[current_pos + 1][0]]]
                if prompt == "":
                    data[pos_to_data[movements[current_pos + 1][0]]] = (
                        "localhost (default)"
                        if editing == "port"
                        else (
                            "3306 (default)"
                            if editing == "username"
                            else "root (default)" if editing == "password" else ""
                        )
                    )
                    colors[2 - current_pos] = curses.color_pair(6)
                elif prompt == "localhost" and editing == "port":
                    data[pos_to_data[movements[current_pos + 1][0]]] += " (default)"
                    colors[2 - current_pos] = curses.color_pair(6)
                    movements[3][1] = 6
                elif prompt == "3306" and editing == "username":
                    data[pos_to_data[movements[current_pos + 1][0]]] += " (default)"
                    colors[2 - current_pos] = curses.color_pair(6)
                    movements[2][1] = 6
                elif prompt == "root" and editing == "password":
                    data[pos_to_data[movements[current_pos + 1][0]]] += " (default)"
                    colors[2 - current_pos] = curses.color_pair(6)
                    movements[1][1] = 10
                else:
                    colors[2 - current_pos] = curses.color_pair(5) | curses.A_ITALIC

            reset_line(stdscr, movements[current_pos + 1][0], 0)
            reset_line(stdscr, movements[current_pos][0], 0)

        elif ch in (curses.KEY_ENTER, 10, 13):
            # Set default values if fields are empty
            if data["host"] == "" or data["host"] == "localhost (default)":
                data["host"] = "localhost"
            if data["port"] == "" or data["port"] == "3306 (default)":
                data["port"] = "3306"
            if data["username"] == "" or data["username"] == "root (default)":
                data["username"] = "root"

            if not (1 <= int(data["port"]) <= 65535):
                reset_line(stdscr, 7, 0)
                addstr(stdscr, 7, 0, "[!] Invalid port", curses.color_pair(3))

            elif len(data["username"]) > 32:
                reset_line(stdscr, 7, 0)
                addstr(
                    stdscr,
                    7,
                    0,
                    "[!] Username cannot be greater than 32 characters",
                    curses.color_pair(3),
                )

            else:
                #* Verify connection
                import mysql.connector

                try:
                    connection = mysql.connector.connect(
                        host=data["host"],
                        port=data["port"],
                        user=data["username"],
                        password=data["password"],
                    )
                    connection.close()
                    reset_line(stdscr, 7, 0)
                    addstr(
                        stdscr,
                        7,
                        0,
                        "[\u2713] Connection successful!",
                        curses.color_pair(2),
                    )
                    addstr(stdscr, 8, 0, "Press any key to continue...")
                    getch(stdscr)
                    break

                except mysql.connector.Error:
                    reset_line(stdscr, 7, 0)
                    addstr(
                        stdscr,
                        7,
                        0,
                        f"[!] Connection with MySQL server failed.",
                        curses.color_pair(3),
                    )

        else:
            #* Edit mode
            editing = pos_to_data[movements[current_pos][0]]

            def handle_key_press(allowable_characters):
                if chr(ch) in allowable_characters:
                    data[editing] += chr(ch)
                    movements[current_pos][1] += 1

                elif ch in (curses.KEY_BACKSPACE, 127, 8):
                    if data[editing]:
                        data[editing] = data[editing][:-1]
                        movements[current_pos][1] -= 1

            if editing == "password":
                handle_key_press("".join(chr(i) for i in range(32, 127)))

            elif editing == "username":
                handle_key_press(
                    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$@.-"
                )

            elif editing == "port":
                handle_key_press("0123456789")

            elif editing == "host":
                handle_key_press(
                    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._"
                )

            reset_line(stdscr, movements[current_pos][0], 0)

    from pickle import dump
    from os import makedirs, urandom
    from scripts.encryption import get_fernet_key
    from csv import writer

    app_salt_file = "appdata/app_salt.dat"
    app_master_password = "seal_app_encryption_secret"

    appdata_dir = "appdata"
    makedirs(appdata_dir, exist_ok=True)

    salt = urandom(16)
    with open(app_salt_file, "wb") as f:
        dump(salt, f)  #* Creating a salt for the global app master password

    fernet = get_fernet_key(app_master_password, app_salt_file)

    #* Encrypted SQL data
    encrypted_sql_data = [
        fernet.encrypt(data["host"].encode()),
        fernet.encrypt(data["port"].encode()),
        fernet.encrypt(data["username"].encode()),
        fernet.encrypt(data["password"].encode())
    ]

    #* Save encrypted data
    with open("appdata/seal_core.csv", "w", newline="") as f:
        writer = writer(f)
        writer.writerow(encrypted_sql_data)


def log_in(stdscr):
    #! Clear the terminal
    stdscr.clear()
    username = ""
    password = ""
    show_password = False
    movements = [[2, 10], [5, 10]]
    current_pos = 0
    pos_to_data = {0: "username", 1: "password"}

    from csv import reader
    with open("appdata/seal_core.csv", "r") as f:
        reader = list(reader(f))

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
            addstr(
                stdscr, 5, 0, f"Password: {"*" * len(password)}"
            )

        move(stdscr, *movements[current_pos])
        ch = getch(stdscr)
        if ch == curses.KEY_RESIZE:
            continue

        if ch == curses.KEY_F2: #* F2 key
            show_password = not show_password

        elif ch == curses.KEY_UP or ch == 353: #* 353 is Shift+Tab in curses
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

            from hashlib import sha256

            skip = True
            username_hash = sha256(username.encode()).hexdigest()
            password_hash = sha256(password.encode()).hexdigest()

            for row in reader:
                if skip:
                    skip = False #* Skip the SQL row
                    continue

                if row[0] == username_hash and row[1] == password_hash:
                    #* Successful login
                    reset_line(stdscr, 7, 0)
                    addstr(
                        stdscr,
                        7,
                        0,
                        "Welcome back, " + username,
                        curses.color_pair(2),
                    )
                    addstr(stdscr, 8, 0, "Press any key to continue...")
                    getch(stdscr)
                    break
            else:
                #* Failed login
                reset_line(stdscr, 7, 0)
                addstr(stdscr, 7, 0, "Invalid username or password.", curses.color_pair(3))
                continue

            break

        else:
            #* Edit mode
            editing = pos_to_data[current_pos]
            if editing == "username":
                if 32 <= ch <= 126: #* Printable ASCII characters
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
    #TODO: Remove this clear when enter vault is implemented
    stdscr.clear()
