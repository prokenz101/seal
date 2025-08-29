def exception_handler(message="Something went wrong.", Exception=None):
    """Handle exceptions and display an error message."""

    print("\033[91m\033[1m[Fatal Error]\033[0m")  #* Red color
    print()
    print(message)
    print()
    if Exception:
        print("\033[93mFull error details:\033[0m")
        print(Exception)
        print()
    exit()


def rgb_to_curses_color(r, g, b):
    """Convert RGB color values to curses color format."""

    return int(r * 1000 / 255), int(g * 1000 / 255), int(b * 1000 / 255)


def accounts_exist():
    """Check if any user accounts exist."""

    from os import path, listdir
    from re import compile

    if path.exists("salts"):
        salts_dir_files = listdir("salts")
        if any(f.endswith(".dat") for f in salts_dir_files):
            hash_pattern = compile(r"[A-Fa-f0-9]{64}")
            if any(hash_pattern.search(f) for f in salts_dir_files):
                return True
            else:
                exception_handler(
                    message="Invalid account hash found in \033[96m'salts'\033[0m directory."
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
