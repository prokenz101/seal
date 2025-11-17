import mysql.connector
from pickle import load
from hashlib import sha256
from core.utils import delete_salt, update_salt
from core.encryption import get_fernet_key


def add_user(username, password):
    """Add a new user to the database."""

    password_hash = sha256(password.encode()).hexdigest()

    conn = connect_mysql()
    cur = conn.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS seal")
    cur.execute("USE seal")
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (username VARCHAR(16) PRIMARY KEY, password_hash VARCHAR(64))"
    )
    cur.execute(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
        (username, password_hash),
    )
    cur.execute(
        """CREATE TABLE IF NOT EXISTS credentials (
    username VARCHAR(16),
    id INT AUTO_INCREMENT PRIMARY KEY,
    account VARCHAR(512) NOT NULL,
    cred_username VARCHAR(512) NOT NULL,
    cred_password VARCHAR(512) NOT NULL,
    FOREIGN KEY (username)
        REFERENCES users(username)
        ON UPDATE CASCADE
);"""
    )
    conn.commit()
    conn.close()


def delete_user(username):
    """Delete a user from the database."""

    conn = connect_mysql()
    cur = conn.cursor()

    try:
        cur.execute("USE seal")
    except mysql.connector.Error:
        conn.close()
        return

    cur.execute("DELETE FROM credentials WHERE username = %s", (username,))
    cur.execute("DELETE FROM users WHERE username = %s", (username,))
    conn.commit()
    conn.close()

    delete_salt(username)


def change_username(old_username, new_username):
    """Change a user's username in the database."""

    conn = connect_mysql()
    cur = conn.cursor()

    try:
        cur.execute("USE seal")
    except mysql.connector.Error:
        conn.close()
        return

    cur.execute(
        "UPDATE users SET username = %s WHERE username = %s",
        (new_username, old_username),
    )
    cur.execute(
        "UPDATE credentials SET username = %s WHERE username = %s",
        (new_username, old_username),
    )
    conn.commit()
    conn.close()

    update_salt(old_username, new_username)


def change_master_password(username, old_password, new_password):
    """Change a user's master password in the database."""

    #* Verify old credentials
    if not account_exists(username, old_password):
        return False

    salt_file = f"data/salts/{username}_salt.dat"
    f_old = get_fernet_key(old_password, salt_file)
    f_new = get_fernet_key(new_password, salt_file)

    conn = connect_mysql()
    cur = conn.cursor()
    try:
        cur.execute("USE seal")
        cur.execute(
            "SELECT id, account, cred_username, cred_password FROM credentials WHERE username = %s",
            (username,),
        )
        rows = cur.fetchall()

        #* Decrypt all existing entries
        decrypted = []
        for id, acc, u, p in rows:
            try:
                d_acc = f_old.decrypt(str(acc).encode()).decode()
                d_user = f_old.decrypt(str(u).encode()).decode()
                d_pass = f_old.decrypt(str(p).encode()).decode()
            except Exception:
                conn.close()
                return False
            decrypted.append((id, d_acc, d_user, d_pass))

        cur.execute("DELETE FROM credentials WHERE username = %s", (username,))

        for id, d_acc, d_user, d_pass in decrypted:
            enc_acc = f_new.encrypt(d_acc.encode()).decode()
            enc_user = f_new.encrypt(d_user.encode()).decode()
            enc_pass = f_new.encrypt(d_pass.encode()).decode()
            cur.execute(
                "INSERT INTO credentials VALUES (%s, %s, %s, %s, %s)",
                (username, id, enc_acc, enc_user, enc_pass),
            )

        #* Update master password hash
        new_hash = sha256(new_password.encode()).hexdigest()
        cur.execute(
            "UPDATE users SET password_hash = %s WHERE username = %s",
            (new_hash, username),
        )

        conn.commit()

    finally:
        conn.close()


def get_usernames():
    """Retrieve a list of all usernames from the database."""

    conn = connect_mysql()
    cur = conn.cursor()

    try:
        cur.execute("USE seal")
    except mysql.connector.Error:
        return []

    cur.execute("SELECT username FROM users")
    results = cur.fetchall()
    conn.close()

    usernames = [username for (username,) in results]

    return usernames


def get_mysql_credentials():
    """Retrieve MySQL credentials from the encrypted CSV file."""

    app_salt_file = "data/appdata/app_salt.dat"
    app_master_password = "seal_app_encryption_secret"

    fernet = get_fernet_key(app_master_password, app_salt_file)
    encrypted_data = []

    with open("data/appdata/mysql.dat", "rb") as f:
        encrypted_data = load(f)

    decrypted_data = (
        fernet.decrypt(encrypted_data[0]).decode(),
        fernet.decrypt(encrypted_data[1]).decode(),
        fernet.decrypt(encrypted_data[2]).decode(),
        fernet.decrypt(encrypted_data[3]).decode(),
    )

    return (decrypted_data[0], decrypted_data[1], decrypted_data[2], decrypted_data[3])


def connect_mysql():
    """Establish and return a MySQL connection using stored credentials."""

    host, port, sqlusername, sqlpassword = get_mysql_credentials()

    conn = mysql.connector.connect(
        host=host, port=int(port), user=sqlusername, password=sqlpassword
    )

    return conn


def account_exists(username, password):
    """Verify user credentials against the database."""

    password_hash = sha256(password.encode()).hexdigest()

    conn = connect_mysql()
    cur = conn.cursor()

    try:
        cur.execute("USE seal")
    except mysql.connector.Error:
        conn.close()
        return False

    cur.execute(
        "SELECT * FROM users WHERE username = %s AND password_hash = %s",
        (username, password_hash),
    )
    result = cur.fetchone()
    conn.close()

    return result is not None


def username_exists(username):
    """Check if a username already exists in the database."""

    conn = connect_mysql()
    cur = conn.cursor()

    try:
        cur.execute("USE seal")
    except mysql.connector.Error:
        return False

    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    result = cur.fetchone()
    conn.close()

    return result is not None


def add_credential(conn, username, account, acc_username, acc_password):
    """Add a new credential entry to the locker table."""

    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO locker (owner, account, username, password)
        VALUES (%s, %s, %s, %s)
    """,
        (username, account, acc_username, acc_password),
    )
    conn.commit()
    conn.close()


def get_credentials_row_count(username, page, page_size: int = 12):
    """Returns the number of rows in a specific page for the user's credentials.

    - page: 1-based page index
    - page_size: items per page (default 12)
    """

    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute("USE seal")
    cursor.execute("SELECT COUNT(*) FROM credentials WHERE username = %s", (username,))
    count = cursor.fetchone()
    conn.close()
    if count is None:
        return 0

    total = int(count[0])  # type: ignore
    if total == 0:
        return 0

    # Clamp page bounds
    total_pages = (total + page_size - 1) // page_size
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    start_idx = (page - 1) * page_size
    remaining = max(0, total - start_idx)
    return min(page_size, remaining)


def get_page_count(username, page_size: int = 12) -> int:
    """Returns total number of pages for the user's credentials.

    - page_size: items per page (default 12)
    """

    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute("USE seal")
    cursor.execute("SELECT COUNT(*) FROM credentials WHERE username = %s", (username,))
    count = cursor.fetchone()
    conn.close()

    total = int(count[0]) if count else 0  # type: ignore[index,arg-type]
    if total == 0:
        return 0
    return (total + page_size - 1) // page_size


def get_credential_row(fernet, username, row_number):
    """Returns the decrypted account, user ID, and password
    for a specific row (1-based) belonging to the given username.
    """
    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute("USE seal")

    cursor.execute(
        "SELECT id, account, cred_username, cred_password "
        "FROM credentials WHERE username = %s",
        (username,),
    )

    results = cursor.fetchall()
    conn.close()

    if not results or row_number <= 0 or row_number > len(results):
        return None

    row = results[row_number - 1]
    id = row[0]

    try:
        account = fernet.decrypt(str(row[1]).encode()).decode()
    except Exception:
        account = "[decryption failed]"

    try:
        user_id = fernet.decrypt(str(row[2]).encode()).decode()
    except Exception:
        user_id = "[decryption failed]"

    try:
        password = fernet.decrypt(str(row[3]).encode()).decode()
    except Exception:
        password = "[decryption failed]"

    return account, user_id, password, id


def get_table(
    fernet,
    tablename,
    database,
    page,
    shown_row=0,
    hide=True,
    select_command=None,
):
    """Tabulates and returns a table with truncation.
    Decrypts all fields using decrypt()."""

    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute(f"USE {database}")

    if select_command is not None:
        cursor.execute(*select_command)
    else:
        cursor.execute(f"SELECT * FROM {tablename}")

    results = cursor.fetchall()

    total_rows = len(results)
    if total_rows == 0:
        conn.close()
        return "(empty table)\nPage (0/0)"

    page_size = 12
    total_pages = (total_rows + page_size - 1) // page_size
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, total_rows)
    page_results = results[start_idx:end_idx]

    limits = {
        "App or website name": 20,
        "User ID": 20,
        "Password": 20,
    }

    #* Column names
    columns = [cd[0] for cd in (cursor.description or [])]

    widths = [len(name) for name in columns]

    #* Decrypt once and apply truncation only while updating widths
    processed_rows = []
    for row_index, row in enumerate(page_results, start=1):
        processed_row = []
        for col_idx, raw_value in enumerate(row):
            col_name = columns[col_idx]
            limit = limits.get(col_name, None)
            value_str = str(raw_value)
            if col_name.lower() == "password":
                if hide or shown_row <= 0 or row_index != shown_row:
                    value_str = "*" * 16
                else:
                    try:
                        value_str = fernet.decrypt(value_str.encode()).decode()
                    except Exception:
                        value_str = "[decryption failed]"
            else:
                try:
                    value_str = fernet.decrypt(value_str.encode()).decode()
                except Exception:
                    value_str = "[decryption failed]"

            if limit and len(value_str) > limit:
                value_str = value_str[: limit - 3] + "..."

            widths[col_idx] = max(widths[col_idx], len(value_str))
            if limit:
                widths[col_idx] = min(widths[col_idx], limit)

            processed_row.append(value_str)
        processed_rows.append(processed_row)

    pipe = "|"
    separator = "+"
    for w in widths:
        pipe += " %-" + f"{w}s |"
        separator += "-" * (w + 2) + "+"

    #* Assemble the table
    table_lines = [separator, pipe % tuple(columns), separator]
    for processed_row in processed_rows:
        table_lines.append(pipe % tuple(processed_row))
    table_lines.append(separator)
    table_lines.append(f"Page ({page}/{total_pages})")

    conn.close()
    return "\n".join(table_lines)
