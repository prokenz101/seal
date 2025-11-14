                            create_salt(username)

                            reset_line(stdscr, 13, 0)
                            addstr(
                                stdscr,
                                14,
                                0,
                                "[\u2713] Password set successfully!",
                                curses.color_pair(2),
                                reset=True
                            )
                            addstr(stdscr, 15, 0, "Press any key to continue...")
                            reset_footer(stdscr)
                            getch(stdscr)

                            from core.sqlutils import add_user

                            add_user(username, master_password)

                            stdscr.clear()
                            stdscr.refresh()
                            addstr(stdscr, 0, 0, "seal", curses.color_pair(4) | curses.A_BOLD)
                            addstr(
                                stdscr,
                                2,
                                0,
                                "[\u2713] Account registered successfully!",
                                curses.color_pair(2),
                            )
                            registered = True
                            addstr(stdscr, 4, 0, "You may now log in.")
                            addstr(stdscr, 5, 0, "Press any key to continue...")
                            getch(stdscr)
                            normal_launch(stdscr, welcome=f"Welcome, {username}!")
                            break
