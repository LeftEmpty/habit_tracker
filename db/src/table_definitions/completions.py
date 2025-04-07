completions: str = """
    CREATE TABLE IF NOT EXISTS completions (
        date TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        habit_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES user(user_id),
        FOREIGN KEY(habit_id) REFERENCES habit(habit_id)
    )
"""