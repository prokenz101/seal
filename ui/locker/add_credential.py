import curses

from core.cutils import (
    addlines,
    addstr,
    addstr_bottom,
    footer,
    getch,
    move,
    reset_line,
    reset_line_bottom,
)
from core.utils import exception_handler


def add_credential(
    stdscr,
    username,
    master_password,
    add_or_edit="Add",
    app="",
    user_id="",
    password="",
    id=None,
):
    """UI for adding or editing a credential."""

    #! Clear the terminal
    stdscr.clear()

    strong_password = ""
    show_password = True
    movements = [[4, 21 + len(app)], [6, 9 + len(user_id)], [9, 10 + len(password)]]
    current_pos = 0
    pos_to_data = {0: "app", 1: "user_id", 2: "password"}
    messages = (
        (0, "          [F3] Suggest strong password"),
        (43, "[F4] Use strong password", curses.color_pair(6) | curses.A_ITALIC),
    )
    hide_or_show = "Hide"

    while True:
        addstr(stdscr, 0, 0, "seal", curses.color_pair(4) | curses.A_BOLD)
        addstr(
            stdscr,
            0,
            4,
            f" — Logged in as {username} — Locker — {add_or_edit} Credential",
            curses.A_BOLD,
        )
        addstr_bottom(
            stdscr,
            2,
            0,
            f"Commands: [F2] {hide_or_show} password               [▲ ▼] Navigate",
        )
        addstr_bottom(stdscr, 1, *messages[0])
        addstr_bottom(stdscr, 1, *messages[1])
        addstr_bottom(
            stdscr, 0, 0, "          [Enter] Confirm                  [ESC] Discard"
        )

        addstr(stdscr, 2, 0, f"{add_or_edit} Credential:", curses.A_BOLD)
        addstr(stdscr, 4, 0, f"App or website name: {app}")
        addstr(stdscr, 6, 0, f"User ID: {user_id}")
        addstr(
            stdscr,
            8,
            0,
            f"Press [F2] to {hide_or_show.lower()} password",
            curses.color_pair(6),
        )

        if show_password:
            addstr(stdscr, 9, 0, f"Password: {password}")
            reset_line(stdscr, 10, 0)
            if strong_password != "":
                addstr(stdscr, 10, 0, f"Strong password: {strong_password}")
        else:
            addstr(stdscr, 9, 0, f"Password: {'*' * len(password)}")
            if strong_password != "":
                addstr(
                    stdscr,
                    10,
                    0,
                    f"Strong password: {'*' * len(strong_password)}",
                )

        move(stdscr, *movements[current_pos])
        ch = getch(stdscr)
        if ch == curses.KEY_RESIZE:
            continue

        if ch == curses.KEY_F2:  #* F2 key
            show_password = not show_password
            hide_or_show = "Hide" if show_password else "Show"

        elif ch == curses.KEY_UP:
            if current_pos > 0:
                current_pos -= 1
                reset_line(stdscr, movements[current_pos + 1][0], 0)
                reset_line(stdscr, movements[current_pos][0], 0)

        elif ch == curses.KEY_DOWN or ch == 9:
            if current_pos < 2:
                current_pos += 1
                reset_line(stdscr, movements[current_pos - 1][0], 0)
                reset_line(stdscr, movements[current_pos][0], 0)

        elif ch == curses.KEY_F3:  #* F3 key
            from core.utils import generate_password

            strong_password = generate_password()
            reset_line_bottom(stdscr, 1, 0)
            messages = (
                (0, "          [F3] Regenerate strong password"),
                (43, "[F4] Use strong password", curses.A_BOLD | curses.A_UNDERLINE),
            )

        elif ch == curses.KEY_F4:  #* F4 key
            if strong_password != "":
                password = strong_password
                strong_password = ""
                reset_line(stdscr, 9, 0)
                reset_line(stdscr, 10, 0)
                reset_line_bottom(stdscr, 1, 0)

                messages = (
                    (0, "          [F3] Suggest strong password"),
                    (
                        43,
                        "[F4] Use strong password",
                        curses.color_pair(6) | curses.A_ITALIC,
                    ),
                )

                movements[2][1] = 20 + 10
                #* Length of password is 20, "Password: " is 10 characters

        elif ch == 27:  #* ESC key
            stdscr.clear()
            break

        elif ch in (curses.KEY_ENTER, 10, 13):
            msg = None
            if password == "":
                msg = "Please type a valid password."
            elif user_id == "":
                msg = "Please type a valid user ID."
            elif app == "":
                msg = "Please type a valid app or website name."

            if msg:
                reset_line(stdscr, 10, 0)
                addstr(stdscr, 11, 0, msg, curses.color_pair(3), reset=True)

            else:
                #* Save credential to database
                from core.sqlutils import connect_mysql
                from core.encryption import encrypt

                conn = connect_mysql()
                cur = conn.cursor()
                cur.execute("USE seal")
                try:
                    if add_or_edit == "Add":
                        cur.execute(
                            "INSERT INTO credentials (username, account, cred_username, cred_password) VALUES (%s, %s, %s, %s);",
                            (
                                username,
                                encrypt(username, master_password, app),
                                encrypt(username, master_password, user_id),
                                encrypt(username, master_password, password),
                            )
                        )
                    elif add_or_edit == "Edit":
                        cur.execute(
                            "UPDATE credentials SET account=%s, cred_username=%s, cred_password=%s WHERE username=%s AND id=%s;",
                            (
                                encrypt(username, master_password, app),
                                encrypt(username, master_password, user_id),
                                encrypt(username, master_password, password),
                                username,
                                id,
                            )
                        )

                    conn.commit()
                    conn.close()

                    stdscr.clear()
                    break
                except Exception as e:
                    exception_handler(stdscr, e)

        else:
            #* Edit mode
            editing = pos_to_data[current_pos]
            if editing == "app":
                if (32 <= ch <= 126) and len(app) < 64:
                    app += chr(ch)
                    movements[current_pos][1] += 1
                elif ch in (curses.KEY_BACKSPACE, 127, 8):
                    if app:
                        app = app[:-1]
                        movements[current_pos][1] -= 1

            elif editing == "user_id":
                if (32 <= ch <= 126) and len(user_id) < 64:
                    user_id += chr(ch)
                    movements[current_pos][1] += 1
                elif ch in (curses.KEY_BACKSPACE, 127, 8):
                    if user_id:
                        user_id = user_id[:-1]
                        movements[current_pos][1] -= 1

            elif editing == "password":
                if (32 <= ch <= 126) and len(password) < 64:
                    password += chr(ch)
                    movements[current_pos][1] += 1
                elif ch in (curses.KEY_BACKSPACE, 127, 8):
                    if password:
                        password = password[:-1]
                        movements[current_pos][1] -= 1

            reset_line(stdscr, movements[current_pos][0], 0)


def delete_credential(stdscr, username, app, user_id, password, id):
    """Delete a credential entry from the locker table by ID."""

    #! Clear the terminal
    stdscr.clear()
    current_pos = "no"
    colors = [curses.color_pair(3), curses.color_pair(7) | curses.A_UNDERLINE]
    
    while True:
        addstr(stdscr, 0, 0, "seal", curses.color_pair(4) | curses.A_BOLD)
        addstr(
            stdscr,
            0,
            4,
            f" — Logged in as {username} — Locker — Delete Credential",
            curses.A_BOLD,
        )

        addstr(stdscr, 2, 0, "Are you sure you want to delete the following credential?")
        addlines(stdscr, 4, 0, f"""App or website name: {app}
User ID: {user_id}
Password: {'*' * len(password)}""")

        addstr(stdscr, 8, 0, "Choose an option:")
        addstr(stdscr, 10, 1, "Yes", colors[0])
        addstr(stdscr, 10, 6, "No", colors[1])
        footer(stdscr, "Use [◀] and [▶] arrow keys to navigate, and [Enter] to confirm.")

        ch = getch(stdscr)
        if ch == curses.KEY_RESIZE:
            continue

        if ch == curses.KEY_LEFT:
            if current_pos == "no":
                current_pos = "yes"
                colors[1] = curses.color_pair(5)
                colors[0] = curses.color_pair(8) | curses.A_UNDERLINE
        elif ch == curses.KEY_RIGHT:
            if current_pos == "yes":
                current_pos = "no"
                colors[0] = curses.color_pair(3)
                colors[1] = curses.color_pair(7) | curses.A_UNDERLINE

        elif ch in (curses.KEY_ENTER, 10, 13):
            if current_pos == "yes":
                from core.sqlutils import connect_mysql

                conn = connect_mysql()
                cur = conn.cursor()
                cur.execute("USE seal")
                cur.execute("DELETE FROM credentials WHERE id = %s", (id,))
                conn.commit()
                conn.close()

                addstr(stdscr, 12, 0, "Credential deleted successfully.", curses.color_pair(2))
                addstr(stdscr, 13, 0, "Press any key to continue...", reset=True)

                getch(stdscr)
                stdscr.clear()

            else:
                stdscr.clear()

            break
