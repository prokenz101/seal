            stdscr.clear()
            curses.curs_set(1)
            move(stdscr, 0, 0)

            if colors[0] == curses.color_pair(7) | curses.A_UNDERLINE:
                setup_mysql(stdscr, proceed_to_username=True)
            else:
                curses.endwin()
                exit()
                pass
