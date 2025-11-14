                    reset_line(stdscr, 8, 0)
                    addstr(
                        stdscr,
                        9,
                        0,
                        "[\u2713] Username set successfully!",
                        curses.color_pair(2),
                        reset=True
                    )
                    addstr(stdscr, 10, 0, "Press any key to continue...")
                    reset_footer(stdscr)
                    getch(stdscr)
                    choose_master_password(stdscr, username)
