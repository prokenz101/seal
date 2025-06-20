
import curses

import pyperclip

def welcome(stdscr):
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

        stdscr.refresh()
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
    stdscr.refresh()
    stdscr.addstr("You chose option " + prompt + "!\n", curses.A_BOLD)
    stdscr.getch()
