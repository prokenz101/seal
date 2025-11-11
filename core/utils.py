from os import path, listdir
from pickle import dump
from os import makedirs, urandom, remove


def exception_handler(message="Something went wrong.", exception=None):
    """Handle exceptions and display an error message."""

    print("\033[91m\033[1m[Fatal Error]\033[0m")  #* Red color
    print()
    print(message)
    print()
    if exception:
        print("\033[93mFull error details:\033[0m")
        print(exception)
        print()
    exit()


def rgb_to_curses_color(r, g, b):
    """Convert RGB color values to curses color format."""

    return int(r * 1000 / 255), int(g * 1000 / 255), int(b * 1000 / 255)


def accounts_exist():
    """Check if any user accounts exist."""

    if path.exists("data/salts"):
        try:
            from core.sqlutils import get_usernames
            usernames = get_usernames()
        except Exception as e:
            exception_handler(
                message="Failed to retrieve usernames from the database.", exception=e
            )

        salts_dir_files = listdir("data/salts")
        actual_files = {f for f in salts_dir_files if f.endswith(".dat")}
        expected_files = {
            f"{username}_salt.dat" for username in usernames # type: ignore
        }

        if not expected_files:
            return False

        if actual_files == expected_files:
            return True
        else:
            exception_handler(
                message="Invalid account salts found in \033[96m'data/salts'\033[0m directory."
            )
    else:
        return False


def is_all_modules_installed():
    """Check if all required modules are installed."""

    modules = {"windows_curses": False, "cryptography": False, "mysql.connector": False}
    #* Testing if individual modules are installed

    try:
        from curses import A_ALTCHARSET

        modules["windows_curses"] = True
    except ModuleNotFoundError:
        pass

    try:
        from cryptography import __version__

        modules["cryptography"] = True
    except ModuleNotFoundError:
        pass

    try:
        from mysql.connector import connect

        modules["mysql.connector"] = True
    except ModuleNotFoundError:
        pass

    if not all(modules.values()):
        print("\033[91m\033[1m[Fatal Error]\033[0m\n")
        print("\033[96mThe following required modules are not installed:\033[0m\n")
        for module in modules:
            if not modules[module]:
                print(f"- \033[93m{module}\033[0m")

        print("\n\033[96mPlease install them using the following command:\033[0m")
        print("'\033[92mpip install -r requirements.txt\033[0m'\n")

        return False

    return True


def get_table(conn, tablename, database=None) -> str | None:
    cursor = conn.cursor()
    if database is not None:
        cursor.execute("USE {}".format(database))
    else:
        return

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
