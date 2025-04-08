habit: str = """
    CREATE TABLE IF NOT EXISTS habit(
        habit_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        frequency INTEGER NOT NULL,
        timeframe TEXT NOT NULL
        )"""
