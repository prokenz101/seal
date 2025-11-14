            stdscr.clear()
            curses.curs_set(1)
            move(stdscr, 0, 0)
            if colors[0] == curses.color_pair(7) | curses.A_UNDERLINE:
                log_in(stdscr, welcome)

            elif colors[1] == curses.color_pair(7) | curses.A_UNDERLINE:
                from ui.setup.username import choose_username

                choose_username(stdscr)

            elif colors[2] == curses.color_pair(7) | curses.A_UNDERLINE:
                sql_warning(stdscr)

            else:
                #! Exiting...
                curses.endwin()
                exit()
                pass
