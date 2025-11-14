                            "INSERT INTO credentials (username, account, cred_username, cred_password) VALUES (%s, %s, %s, %s);",
                            (
                                username,
                                encrypt(username, master_password, app),
                                encrypt(username, master_password, user_id),
                                encrypt(username, master_password, password),
                            )
                        )
                    elif add_or_edit == "Edit":
                        cur.execute(
                            "UPDATE credentials SET account=%s, cred_username=%s, cred_password=%s WHERE username=%s AND id=%s;",
                            (
                                encrypt(username, master_password, app),
                                encrypt(username, master_password, user_id),
                                encrypt(username, master_password, password),
                                username,
                                id,
                            )
                        )
