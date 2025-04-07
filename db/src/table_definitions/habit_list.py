habit_list: str = """
    CREATE TABLE IF NOT EXISTS habit_list (
        start_date TEXT NOT NULL,
        last_updated_on TEXT NOT NULL,
        streak INTEGER NOT NULL,
        highest_streak INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        habit_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES user(user_id),
        FOREIGN KEY(habit_id) REFERENCES habit(habit_id)        
    )
"""