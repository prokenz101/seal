
import curses

def welcome(stdscr):
    #! Clear the terminal
    stdscr.clear()

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
    stdscr.addstr(9, 0, "Press any key to continue...")

    stdscr.refresh()
    stdscr.getch()  #* Wait for user key press
