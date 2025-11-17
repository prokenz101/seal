from pickle import dump
from string import ascii_letters, digits
from os import makedirs, urandom, remove, rename, path, listdir


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

        #* Specific MySQL related error
        if str(exception) == "Authentication plugin 'caching_sha2_password' is not supported":
            print("\033[92mTip:\033[0m")
            print("\033[93m1. Try uninstalling mysql.connector with:\033[0m")
            print("   '\033[96mpip uninstall mysql.connector\033[0m'")
            print("\033[93m2. Then, install mysql-connector-python with:\033[0m")
            print("   '\033[96mpip install mysql-connector-python\033[0m'")

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

    modules = {"windows_curses": False, "cryptography": False, "mysql.connector": False, "pyperclip": False}
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

    try:
        from pyperclip import copy

        modules["pyperclip"] = True
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


def update_salt(old_username, new_username):
    """Update the salt file when the username changes."""

    old_salt_path = f"data/salts/{old_username}_salt.dat"
    new_salt_path = f"data/salts/{new_username}_salt.dat"

    if path.exists(old_salt_path):
        try:
            rename(old_salt_path, new_salt_path)
        except Exception as e:
            exception_handler(
                message=f"Failed to update salt file from '{old_username}' to '{new_username}'.", exception=e
            )


def generate_password(length=20):
    alphabet = ascii_letters + digits + "._$%"
    random_bytes = urandom(length)
    password = ''.join(alphabet[b % len(alphabet)] for b in random_bytes)
    return password
