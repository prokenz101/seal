import curses
from core.utils import exception_handler

#* cutils -> utilities involving curses module


def setup_colors(stdscr):
    "Sets up all color pairs and handles terminals that do not support colors."

    curses.start_color()

    if curses.can_change_color():
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

        curses.init_pair(4, 11, curses.COLOR_BLACK)

        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(6, 8, curses.COLOR_BLACK)  #* gray
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    else:
        stdscr.clear()
        exception_handler(
            message="\033[96mYour terminal does not support colored text.\033[0m"
        )


def check_terminal_size(stdscr):
    """Check if terminal window is larger than 25x85 characters."""
    max_y, max_x = stdscr.getmaxyx()
    if max_y < 25 or max_x < 85:
        raise curses.error("Terminal window is too small to display text.")


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


def addstr(stdscr, y, x, string, attr=curses.A_NORMAL, reset=False):
    """Add a string to the specified position without going out of bounds."""

    max_y, max_x = stdscr.getmaxyx()
    if 0 <= y < max_y and 0 <= x + len(string) < max_x:
        if reset:
            reset_line(stdscr, y, x)
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


def reset_line_bottom(stdscr, y, x):
    """Clear a specific line relative to the bottom of the screen."""

    max_y = stdscr.getmaxyx()[0]
    target_y = max_y - 1 - y
    move(stdscr, target_y, x)
    stdscr.clrtoeol()


def reset_lines(stdscr, *lines):
    """Clear multiple specific lines.

    Args:
        *lines: A list of tuples containing (stdscr, y, x) for each line to reset.
    """

    for y, x in lines:
        reset_line(stdscr, y, x)


def footer(stdscr, message, attr=curses.A_NORMAL):
    """Display a footer message at the bottom of the screen."""

    max_y = stdscr.getmaxyx()[0]
    reset_line(stdscr, max_y - 1, 0)
    addstr(stdscr, max_y - 1, 0, message, attr)
    stdscr.refresh()


def reset_footer(stdscr):
    """Clear the footer line."""

    max_y = stdscr.getmaxyx()[0]
    reset_line(stdscr, max_y - 1, 0)


def addstr_bottom(stdscr, y, x, message, attr=curses.A_NORMAL):
    """Add a string relative to the bottom of the screen."""

    max_y = stdscr.getmaxyx()[0]
    max_y, max_x = stdscr.getmaxyx()
    target_y = max_y - 1 - y
    if 0 <= target_y < max_y and 0 <= x + len(message) < max_x:
        stdscr.addstr(target_y, x, message, attr)
    else:
        raise curses.error("Terminal window is too small to display text.")
