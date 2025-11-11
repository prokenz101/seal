import curses
from time import sleep
import mysql.connector
from pickle import dump
from os import makedirs, urandom
from core.encryption import get_fernet_key
from core.cutils import addlines, addstr, move, footer, getch, reset_line


def setup_mysql(stdscr):
    """Set up the MySQL connection parameters."""

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


    app_salt_file = "data/appdata/app_salt.dat"
    app_master_password = "seal_app_encryption_secret"

    appdata_dir = "data/appdata"
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
        fernet.encrypt(data["password"].encode()),
    ]

   #* Save encrypted data
    with open("data/appdata/mysql.dat", "wb") as f:
        dump(encrypted_sql_data, f)


def sql_warning(stdscr):
    #! Clear the terminal
    stdscr.clear()

    while True:
        addstr(stdscr, 1, 0, "Warning:", curses.color_pair(3) | curses.A_BOLD)
        addlines(
            stdscr,
            2,
            0,
            """Changing your MySQL connection settings may affect access to
your stored password data. """,
            curses.A_BOLD,
        )
        addstr(
            stdscr,
            3,
            27,
            "If the new server address, username,",
            curses.A_BOLD | curses.A_UNDERLINE,
        )
        addlines(
            stdscr,
            4,
            0,
            """or password is incorrect, seal will not be able to connect to
the database that stores your saved accounts.""",
            curses.A_BOLD | curses.A_UNDERLINE,
        )
        addlines(
            stdscr,
            7,
            0,
            """If the new settings do not match the actual database setup,
your saved data may become permanently inaccessible.

Proceed only if you are certain the new connection details
are correct.""",
            curses.A_BOLD,
        )

        stdscr.refresh()
        sleep(3)
        stdscr.addstr(
            14,
            0,
            "Press [ESC] to go back, or any other key to continue...",
            curses.A_BOLD,
        )

        ch = getch(stdscr)
        if ch == curses.KEY_RESIZE:
            continue

        if ch != 27: #* ESC key
            setup_mysql(stdscr)

        break
