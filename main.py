from scripts.utils import exit_seal, exception_handler, rgb_to_curses_color, is_all_modules_installed


def main(stdscr):
    #* Set up color pairs for colorful text
    curses.start_color()

    if curses.can_change_color():
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        curses.init_color(11, *rgb_to_curses_color(125, 229, 255))  #* teal
        curses.init_pair(4, 11, curses.COLOR_BLACK)

        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
    else:
        stdscr.clear()
        exception_handler(
            message="\033[96mYour terminal does not support colored text.\033[0m"
        )

    #* Start SEAL

    try:
        # from scripts.encryption import encrypt, decrypt
        from scripts.menu import first_time_launch
        from re import compile
        from os import path, listdir

        #* Check if an account exists
        
        if path.exists("salts"):
            salts_dir_files = listdir("salts")
            if any(f.endswith('.dat') for f in salts_dir_files):
                hash_pattern = compile(r"[A-Fa-f0-9]{64}")
                if any(hash_pattern.search(f) for f in salts_dir_files):
                    normal_launch(stdscr)
                else:
                    exception_handler(message="\033[96mInvalid account hash found in 'salts' directory.\033[0m")
        else:
            first_time_launch(stdscr)

        # encrypt(
        #     username,
        #     password,
        #     [
        #         ["Outlook", "john@outlook.com", "InD9RQSVF0ZJ3up6", "azure"],
        #         ["Google", "john@gmail.com", "FtF9VDFnxMMgzVlE", "green"],
        #         ["Steam", "john@gmail.com", "lC3NdFOXXG9a9FHe", "blue"],
        #     ],
        # )
        # decrypt(username, password)

    except ModuleNotFoundError as e:
        missing_file = str(e).split("'")[1].split(".")[1]
        exception_handler(
            message=f"\033[96mMissing required file '\033[92mscripts/{missing_file}.py\033[96m'. Please restore or re-download it.\033[0m",
            Exception=e,
        )
    except Exception as e:
        exception_handler(Exception=e)


try:
    from sys import modules
    from os import path, system

    if "idlelib.run" in modules:
        #! Program runs itself in a terminal if it is run in IDLE
        #! This is because IDLE does not support curses, or colored text
        script = path.abspath(__file__) #* Path of main.py
        system(f"start \"\" py \"{script}\"")

if is_all_modules_installed():
    import curses
    from cryptography import __version__ #* Importing nothing from cryptography, just checking if it is installed

    stdscr = curses.initscr()  #* Initialize the curses
    curses.noecho()  #* Hides user inputs
    curses.cbreak()  #* React to keys instantly
    stdscr.keypad(True)  #* Enable the keypad keys

    curses.wrapper(main)
    exit_seal(stdscr)
