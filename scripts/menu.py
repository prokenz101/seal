import curses
from scripts.utils import reset_line
from scripts.user import choose_username


def first_time_launch(stdscr):
    #! Clear the terminal
    stdscr.clear()

    colors = [curses.color_pair(5), curses.color_pair(5)]
    prompt = ""

    while True:
        stdscr.addstr(0, 11, "Welcome to", curses.A_BOLD)
        stdscr.move(1, 0)
        stdscr.clrtoeol()
        stdscr.addstr(2, 0, "███████╗███████╗ █████╗ ██╗     ", curses.color_pair(4))
        stdscr.addstr(3, 0, "██╔════╝██╔════╝██╔══██╗██║     ", curses.color_pair(4))
        stdscr.addstr(4, 0, "███████╗█████╗  ███████║██║     ", curses.color_pair(4))
        stdscr.addstr(5, 0, "╚════██║██╔══╝  ██╔══██║██║     ", curses.color_pair(4))
        stdscr.addstr(6, 0, "███████║███████╗██║  ██║███████╗", curses.color_pair(4))
        stdscr.addstr(7, 0, "╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝", curses.color_pair(4))
        stdscr.move(8, 0)
        stdscr.clrtoeol()
        stdscr.move(9, 0)
        stdscr.clrtoeol()
        stdscr.addstr(10, 0, "Choose an option:")
        stdscr.addstr(11, 0, "1. Get Started", colors[0])
        stdscr.addstr(12, 0, "2. Exit", colors[1])
        stdscr.move(13, 0)
        stdscr.clrtoeol()
        stdscr.addstr(14, 0, ">")
        stdscr.move(14, 2)

        # stdscr.refresh()
        stdscr.addstr(14, 1, " " + prompt + " ")
        stdscr.move(14, 2 + len(prompt))  #* Move cursor to end of prompt
        ch = stdscr.getch()  #* Wait for user key press

        #* If Enter is pressed and requirement is met, exit loop
        if (ch in (curses.KEY_ENTER, 10, 13)) and (prompt == "1" or prompt == "2"):
            break

        #* Handle backspace
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            colors = [curses.color_pair(5), curses.color_pair(5)]
            prompt = ""

        #* Accepts only numbers and lowercase letters, so long as the user is allowed to type
        elif ch == ord("1") or ch == ord("2"):
            prompt = chr(ch)
            colors = [curses.color_pair(5), curses.color_pair(5)]
            colors[int(prompt) - 1] = curses.color_pair(4)

    stdscr.clear()
    stdscr.move(0, 0)
    # stdscr.refresh()
    if prompt == "1":
        setup_my_sql(stdscr)
        # choose_username(stdscr)
    elif prompt == "2":
        #! Exiting...
        pass


def normal_launch(stdscr):
    #! Clear the terminal
    stdscr.clear()

    colors = [curses.color_pair(5), curses.color_pair(5)]
    prompt = ""

    while True:
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(1, 0, "███████╗███████╗ █████╗ ██╗     ", curses.color_pair(4))
        stdscr.addstr(2, 0, "██╔════╝██╔════╝██╔══██╗██║     ", curses.color_pair(4))
        stdscr.addstr(3, 0, "███████╗█████╗  ███████║██║     ", curses.color_pair(4))
        stdscr.addstr(4, 0, "╚════██║██╔══╝  ██╔══██║██║     ", curses.color_pair(4))
        stdscr.addstr(5, 0, "███████║███████╗██║  ██║███████╗", curses.color_pair(4))
        stdscr.addstr(6, 0, "╚══════╝╚══════╝╚═╝  ╚═╝╚══════╝", curses.color_pair(4))

        stdscr.move(7, 0)
        stdscr.clrtoeol()
        stdscr.move(8, 0)
        stdscr.clrtoeol()

        stdscr.addstr(9, 0, "Choose an option:")
        stdscr.addstr(10, 0, "1. Enter vault", colors[0])
        stdscr.addstr(11, 0, "2. Exit", colors[1])

        stdscr.move(12, 0)
        stdscr.clrtoeol()

        stdscr.addstr(13, 0, ">")
        stdscr.move(13, 2)
        stdscr.addstr(13, 1, " " + prompt + " ")
        stdscr.move(13, 2 + len(prompt))  #* Move cursor to end of prompt
        stdscr.refresh()

        ch = stdscr.getch()
        #* If Enter is pressed and requirement is met, exit loop
        if (ch in (curses.KEY_ENTER, 10, 13)) and (prompt == "1" or prompt == "2"):
            break

        #* Handle backspace
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            colors = [curses.color_pair(5), curses.color_pair(5)]
            prompt = ""

        #* Accepts only numbers and lowercase letters, so long as the user is allowed to type
        elif ch == ord("1") or ch == ord("2"):
            prompt = chr(ch)
            colors = [curses.color_pair(5), curses.color_pair(5)]
            colors[int(prompt) - 1] = curses.color_pair(4)

    stdscr.clear()
    if prompt == "1":
        enter_vault(stdscr)
    elif prompt == "2":
        pass


def setup_my_sql(stdscr):
    #! Clear the terminal
    stdscr.clear()

    data = {
        "host": "localhost",
        "port": "3306",
        "username": "root",
        "password": "",
    }

    colors = [curses.color_pair(6), curses.color_pair(6), curses.color_pair(6)]
    possible_moving_pos = [[5, 10], [4, 10], [3, 6], [2, 6]]
    current_pos = 0
    pos_to_data = {2: "host", 3: "port", 4: "username", 5: "password"}

    while True:
        for key, default in [("host", "localhost"), ("port", "3306"), ("username", "root")]:
            if data[key] == default:
                data[key] += " (default)"

        stdscr.addstr(0, 0, "Set up MySQL connection:", curses.A_BOLD)
        stdscr.move(1, 0)
        stdscr.clrtoeol()
        stdscr.addstr(2, 0, f"Host: {data['host']}", colors[0])
        stdscr.addstr(3, 0, f"Port: {data['port']}", colors[1])
        stdscr.addstr(4, 0, f"Username: {data['username']}", colors[2])
        stdscr.addstr(5, 0, f"Password: {data['password']}", curses.color_pair(5))

        stdscr.move(*possible_moving_pos[current_pos])
        ch = stdscr.getch()

        if ch == curses.KEY_UP and current_pos < 3:
            current_pos += 1
            colors[3 - current_pos] = curses.color_pair(5)
            if current_pos > 1:
                colors[4 - current_pos] = curses.color_pair(6)

        elif ch == curses.KEY_DOWN and current_pos > 0:
            current_pos -= 1
            colors[2 - current_pos] = curses.color_pair(6)
            if not current_pos == 0:
                colors[3 - current_pos] = curses.color_pair(5)

        elif ch in (curses.KEY_ENTER, 10, 13):
            ...

        else:
            #* Edit mode
            editing = pos_to_data[possible_moving_pos[current_pos][0]]

            if editing == "password":
                # if " (default)" in data[editing]:
                #     data[editing] = ""

                if 32 <= ch <= 126:  #*  Printable ASCII characters
                    data[editing] += chr(ch)
                    possible_moving_pos[current_pos][1] += 1
                    reset_line(stdscr, possible_moving_pos[current_pos][0], 0)

                elif ch in (curses.KEY_BACKSPACE, 127, 8):
                    if data[editing]:
                        data[editing] = data[editing][:-1]
                        possible_moving_pos[current_pos][1] -= 1
                        reset_line(stdscr, possible_moving_pos[current_pos][0], 0)

            elif editing == "username":

                if chr(ch) in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_$@.-":
                    if " (default)" in data[editing]:
                        data[editing] = ""
                        reset_line(stdscr, possible_moving_pos[current_pos][0], 0)
                    data[editing] += chr(ch)
                    possible_moving_pos[current_pos][1] += 1
                    reset_line(stdscr, possible_moving_pos[current_pos][0], 0)

                elif ch in (curses.KEY_BACKSPACE, 127, 8):
                    if data[editing]:
                        data[editing] = data[editing][:-1]
                        possible_moving_pos[current_pos][1] -= 1

                        if data[editing] == "":
                            data[editing] = "localhost"
                        reset_line(stdscr, possible_moving_pos[current_pos][0], 0)


def enter_vault(stdscr):
    #! Clear the terminal
    stdscr.clear()
    stdscr.addstr("Entering vault...\n", curses.A_BOLD)
    stdscr.refresh()
    stdscr.getch()  #* Wait for user to press a key before proceeding
