def exit_curses(stdscr):
    #* Exit the program and restore terminal settings
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
