def get_all_table_defs() -> list[str]:
    return [User, HabitData, HabitSubscription, Completions]

User: str = """
    CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY,
        display_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )"""

HabitData: str = """
    CREATE TABLE IF NOT EXISTS habit_data(
        habit_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    )"""

HabitSubscription: str = """
    CREATE TABLE IF NOT EXISTS habit_subscription (
        habit_sub_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        habit_id INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        latest_date TEXT NOT NULL,
        periodicty TEXT NOT NULL,
        cur_streak INTEGER NOT NULL,
        max_streak INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES User(user_id),
        FOREIGN KEY(habit_id) REFERENCES HabitData(habit_id)
    )"""

Completions: str = """
    CREATE TABLE IF NOT EXISTS completions (
        date TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        habit_sub_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES User(user_id),
        FOREIGN KEY(habit_sub_id) REFERENCES HabitSubscription(habit_sub_id)
    )"""