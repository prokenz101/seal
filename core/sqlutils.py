from pickle import load
import mysql.connector
from hashlib import sha256
from core.utils import delete_salt
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
        host=host,
        port=int(port),
        user=sqlusername,
        password=sqlpassword
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


def get_table(conn, tablename, database=None, select_command=None):
    """Tabulates and returns a table."""
    cur.execute(
        """
        INSERT INTO locker (owner, account, username, password)
        VALUES (%s, %s, %s, %s)
    """,
        (username, account, acc_username, acc_password),
    )

    cursor = conn.cursor()
    if database is not None:
        cursor.execute("USE {}".format(database))
    else:
        return
    cursor.execute("SELECT COUNT(*) FROM credentials WHERE username = %s", (username,))
    cursor.execute("USE seal")
    cursor.execute("SELECT COUNT(*) FROM credentials WHERE username = %s", (username,))
    cursor.execute(
        "SELECT id, account, cred_username, cred_password "
        "FROM credentials WHERE username = %s",
        (username,),
    )

    if select_command is not None:
        cursor.execute(select_command)
    else:
        cursor.execute("SELECT * FROM {}".format(tablename))

    results = cursor.fetchall()

    widths = []
    columns = []
    pipe = "|"
    separator = "+"

    index = 0
    for cd in cursor.description if cursor.description is not None else []:
        widths.append(
            max(
                max(list(map(lambda x: len(str(tuple(x)[index])), results))), len(cd[0])
            )
        )
        columns.append(cd[0])
        index += 1

    for w in widths:
        pipe += " %-" + "%ss |" % (w,)
        separator += "-" * w + "--+"

    table = ""

    table += separator + "\n"
    table += pipe % tuple(columns) + "\n"
    table += separator + "\n"
    for row in results:
        table += pipe % row + "\n"
    table += separator + "\n"

    conn.close()
    return table
