            select_command=("SELECT account AS 'App or website name', cred_username as 'User ID', cred_password as 'Password' FROM credentials WHERE username = %s;",
