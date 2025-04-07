user: str = """
    CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY,
        display_name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )"""