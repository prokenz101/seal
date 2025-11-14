from pickle import dump
from os import path, listdir
from os import makedirs, urandom, remove
from string import ascii_letters, digits


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


def create_salt(username):
    """Create a salt file for the given username."""

    salt = urandom(16)  #* Generate a random 16-byte salt
    makedirs("data/salts", exist_ok=True)

    with open(f"data/salts/{username}_salt.dat", "wb") as f:
        dump(salt, f)


def delete_salt(username):
    """Delete the salt file for the given username."""

    salt_file_path = f"data/salts/{username}_salt.dat"

    if path.exists(salt_file_path):
        try:
            remove(salt_file_path)
        except Exception as e:
            exception_handler(
                message=f"Failed to delete salt file for user '{username}'.", exception=e
            )


def generate_password(length=20):
    alphabet = ascii_letters + digits + "._$%"
    random_bytes = urandom(length)
    password = ''.join(alphabet[b % len(alphabet)] for b in random_bytes)
    return password
