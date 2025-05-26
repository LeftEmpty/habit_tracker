def get_all_table_defs() -> list[str]:
    return [User, HabitData, HabitSubscription, Completions]

User: str = """
    CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        display_name TEXT NOT NULL,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )"""

HabitData: str = """
    CREATE TABLE IF NOT EXISTS habit_data(
        habit_data_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        author_name TEXT NOT NULL,
        author_user_id INTEGER NOT NULL,
        public BOOLEAN DEFAULT FALSE,
        official BOOLEAN DEFAULT FALSE,
        last_modified TEXT,
        FOREIGN KEY(author_user_id) REFERENCES user(user_id)
    )"""

HabitSubscription: str = """
    CREATE TABLE IF NOT EXISTS habit_subscription (
        habit_sub_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        data_id INTEGER NOT NULL,
        periodicity TEXT NOT NULL,
        cur_streak INTEGER NOT NULL,
        max_streak INTEGER NOT NULL,
        creation_date TEXT NOT NULL,
        latest_date TEXT,
        FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE,
        FOREIGN KEY(data_id) REFERENCES HabitData(habit_data_id)
    )"""

Completions: str = """
    CREATE TABLE IF NOT EXISTS completion (
        date TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        habit_sub_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES User(user_id),
        FOREIGN KEY(habit_sub_id) REFERENCES HabitSubscription(habit_sub_id)
    )"""