import curses

from scripts.utils import exception_handler, rgb_to_curses_color

#* cutils -> utilities involving curses module


def setup_colors(stdscr):
    "Sets up all color pairs and handles terminals that do not support colors."

    curses.start_color()

    if curses.can_change_color():
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        curses.init_color(11, *rgb_to_curses_color(125, 229, 255))  #* teal
        curses.init_pair(4, 11, curses.COLOR_BLACK)

        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(6, 8, curses.COLOR_BLACK)  #* gray
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)
    else:
        stdscr.clear()
        exception_handler(
            message="\033[96mYour terminal does not support colored text.\033[0m"
        )


def getch(stdscr):
    """Get a character from the user.

    Handles terminal resize events to prevent out of bounds text."""
    ch = stdscr.getch()
    if ch == curses.KEY_RESIZE:
        stdscr.clear()
        reset_line(stdscr, 0, 0)
        stdscr.addstr(
            0,
            0,
            "Please do not resize the terminal!",
            curses.color_pair(3) | curses.A_UNDERLINE | curses.A_BOLD,
        )
        stdscr.addstr(2, 0, "Press any key to continue...")
        getch(stdscr)
        stdscr.clear()

    return ch


def move(stdscr, y, x):
    """Move the cursor to the specified position without going out of bounds."""

    max_y, max_x = stdscr.getmaxyx()
    if 0 <= y < max_y and 0 <= x < max_x:
        stdscr.move(y, x)
    else:
        raise curses.error("Terminal window is too small to display text.")


def addstr(stdscr, y, x, string, attr=curses.A_NORMAL):
    """Add a string to the specified position without going out of bounds."""

    max_y, max_x = stdscr.getmaxyx()
    if 0 <= y < max_y and 0 <= x + len(string) < max_x:
        stdscr.addstr(y, x, string, attr)
    else:
        raise curses.error("Terminal window is too small to display text.")


def addlines(stdscr, y, x, string: str, attr=curses.A_NORMAL):
    """Add multiple lines of text starting from the specified position."""
    
    lines = string.split("\n")
    longest_line = ""
    #* Get the longest line
    for line in lines:
        if len(line) > len(longest_line):
            longest_line = line

    max_y, max_x = stdscr.getmaxyx()
    if 0 <= y + len(lines) - 1 < max_y and 0 <= x + len(longest_line) - 1 < max_x:
        i = 0
        for line in lines:
            stdscr.addstr(y + i, x, line, attr)
            i += 1
    else:
        raise curses.error("Terminal window is too small to display text.")


def reset_line(stdscr, y, x):
    """Clear a specific line."""

    move(stdscr, y, x)
    stdscr.clrtoeol()


def footer(stdscr, message, attr=curses.A_NORMAL):
    """Display a footer message at the bottom of the screen."""

    max_y = stdscr.getmaxyx()[0]
    reset_line(stdscr, max_y - 1, 0)
    addstr(stdscr, max_y - 1, 0, message, attr)
    stdscr.refresh()
