import curses
from core.cutils import addlines, addstr, addstr_bottom, footer, getch, reset_line
from core.encryption import get_fernet_key
from core.sqlutils import (
    get_credential_row,
    get_page_count,
    get_table,
    get_credentials_row_count,
)
from ui.locker.add_credential import add_credential, delete_credential


def locker(stdscr, username, master_password):
    """Display the locker UI."""

    #! Clear the terminal
    stdscr.clear()

    #* Use one derived Fernet key for all decrypts
    #* Saves on performance since we don't have to derive over and over
    fernet = get_fernet_key(master_password, f"data/salts/{username}_salt.dat")

    pointer = 5
    page = 1
    hide = True
    show_hide = "Show"
    copy_username = "Copy username", curses.A_NORMAL
    copy_password = "Copy password", curses.A_NORMAL
    row_count = get_credentials_row_count(username, page)

    def update_table():
        max_y = stdscr.getmaxyx()[0]
        for y in range(2, max(2, max_y - 4)):
            reset_line(stdscr, y, 0)

        t = get_table(
            fernet,
            "credentials",
            "seal",
            page,
            shown_row=pointer - (12 * (page - 1)) - 4,
            hide=hide,
            select_command=("SELECT account AS 'App or website name', cred_username as 'User ID', cred_password as 'Password' FROM credentials WHERE username = %s;",
                (username,)
            ),
        )
        nonlocal row_count, copy_username, copy_password
        row_count = get_credentials_row_count(username, page)
        copy_username = "Copy username", curses.A_NORMAL
        copy_password = "Copy password", curses.A_NORMAL

        if t != "(empty table)":
            addlines(stdscr, 2, 5, t)

        return t

    table = update_table()

    while True:
        addstr(stdscr, 0, 0, "seal", curses.color_pair(4) | curses.A_BOLD)
        addstr(stdscr, 0, 4, f" — Logged in as {username} — Locker", curses.A_BOLD)

        if table == "(empty table)\nPage (0/0)":
            addlines(
                stdscr,
                2,
                1,
                """It looks like your locker is empty.
Add entries by pressing the 'a' key.""",
            )
            footer(stdscr, "Press [a] to add a new entry, or [ESC] to exit locker.")

        else:
            addstr(stdscr, pointer - 12 * (page - 1), 0, " --> ", curses.A_BOLD)

            addstr_bottom(
                stdscr,
                3,
                0,
                "Commands: [a] Add new entry     [e] Edit selected entry   [d] Delete selected entry",
            )
            addstr_bottom(
                stdscr, 2, 0, "          [▲ ▼] Move pointer    [◀ ▶] Change page"
            )
            addstr_bottom(
                stdscr,
                2,
                58,
                f"[h] {show_hide} credentials",
                curses.A_BOLD | curses.A_UNDERLINE,
            )
            addstr_bottom(stdscr, 1, 10, f"[F4] {copy_username[0]}", copy_username[1])
            addstr_bottom(stdscr, 1, 32, f"[F5] {copy_password[0]}", copy_password[1])
            addstr_bottom(stdscr, 1, 58, "[r] Refresh table")
            addstr_bottom(
                stdscr, 0, 0, "          [ESC] Exit locker     [v] View entry"
            )

        ch = getch(stdscr)
        if ch == curses.KEY_RESIZE:
            continue

        if ch == curses.KEY_DOWN:
            if pointer < (5 + 12 * (page - 1)) + row_count - 1:
                addstr(stdscr, pointer - 12 * (page - 1), 0, "     ")
                copy_username = "Copy username", curses.A_NORMAL
                copy_password = "Copy password", curses.A_NORMAL
                pointer += 1
                if not hide:
                    hide = True
                    table = update_table()
            else:
                if page < get_page_count(username):
                    page += 1
                    pointer += 1
                    table = update_table()

        elif ch == curses.KEY_UP:
            if pointer > 5 + 12 * (page - 1):
                addstr(stdscr, pointer - 12 * (page - 1), 0, "     ")
                copy_username = "Copy username", curses.A_NORMAL
                copy_password = "Copy password", curses.A_NORMAL
                pointer -= 1
                if not hide:
                    hide = True
                    table = update_table()
            else:
                if page > 1:
                    page -= 1
                    pointer -= 1  #* Bottom row
                    table = update_table()

        elif ch == curses.KEY_RIGHT:
            if page < get_page_count(username):
                page += 1
                pointer = 5 + 12 * (page - 1)
                table = update_table()
            
        elif ch == curses.KEY_LEFT:
            if page > 1:
                page -= 1
                pointer = 5 + 12 * (page - 1)
                table = update_table()

        elif ch == curses.KEY_F4:
            row = get_credential_row(fernet, username, pointer - 4)
            if row:
                from pyperclip import copy

                copy(row[1])
                copy_username = "Copied!      ", curses.color_pair(2) | curses.A_BOLD
            else:
                copy_username = "Copy failed  ", curses.color_pair(3) | curses.A_BOLD
            copy_password = "Copy password", curses.A_NORMAL

        elif ch == curses.KEY_F5:
            row = get_credential_row(fernet, username, pointer - 4)
            if row:
                from pyperclip import copy

                copy(row[2])
                copy_password = "Copied!      ", curses.color_pair(2) | curses.A_BOLD
            else:
                copy_password = "Copy failed  ", curses.color_pair(3) | curses.A_BOLD
            copy_username = "Copy username", curses.A_NORMAL

        elif ch in (ord("a"), ord("A")):
            add_credential(stdscr, username, master_password, "Add")
            table = update_table()

        elif ch in (ord("h"), ord("H")):
            hide = not hide
            show_hide = "Hide" if not hide else "Show"
            table = update_table()

        elif ch in (ord("e"), ord("E")):
            row = get_credential_row(fernet, username, pointer - 4)
            if row:
                add_credential(stdscr, username, master_password, "Edit", *row)
                table = update_table()

        elif ch in (ord("d"), ord("D")):
            row = get_credential_row(fernet, username, pointer - 4)
            if row:
                delete_credential(stdscr, username, *row)
                if pointer != 5:
                    pointer -= 1
                table = update_table()

        elif ch in (ord("v"), ord("V")):
            row = get_credential_row(fernet, username, pointer - 4)
            if row:
                stdscr.clear()
                addstr(stdscr, 0, 0, "seal", curses.color_pair(4) | curses.A_BOLD)
                addstr(
                    stdscr,
                    0,
                    4,
                    f" — Logged in as {username} — View Credential",
                    curses.A_BOLD,
                )
                addlines(
                    stdscr,
                    2,
                    0,
                    f"""App or website name: {row[0]}
User ID: {row[1]}
Password: {row[2]}""",
                )
                footer(stdscr, "Press any key to return to locker.")
                getch(stdscr)
                stdscr.clear()
                table = update_table()

        elif ch in (ord("r"), ord("R")):
            table = update_table()

        elif ch == 27:
            stdscr.clear()
            break
