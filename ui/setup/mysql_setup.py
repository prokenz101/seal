            "Use [▲] and [▼] arrow keys to navigate, [ESC] to go back, and [Enter] to confirm.",

                    app_salt_file = "data/appdata/app_salt.dat"
                    app_master_password = "seal_app_encryption_secret"

                    appdata_dir = "data/appdata"
                    makedirs(appdata_dir, exist_ok=True)

                    salt = urandom(16)
                    with open(app_salt_file, "wb") as f:
                        dump(salt, f)  #* Creating a salt for the global app master password

                    fernet = get_fernet_key(app_master_password, app_salt_file)

                    #* Encrypted SQL data
                    encrypted_sql_data = [
                        fernet.encrypt(data["host"].encode()),
                        fernet.encrypt(data["port"].encode()),
                        fernet.encrypt(data["username"].encode()),
                        fernet.encrypt(data["password"].encode()),
                    ]

                    #* Save encrypted data
                    with open("data/appdata/mysql.dat", "wb") as f:
                        dump(encrypted_sql_data, f)

                    if proceed_to_username:
                        from ui.setup.username import choose_username

                        choose_username(stdscr)
