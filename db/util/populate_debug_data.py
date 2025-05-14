import random
import hashlib
from datetime import datetime, timedelta

import db.src.controller as dbc

# Create completions directly via SQL
import sqlite3

PERIODICITIES = ["Daily", "Weekly", "Every Monday", "Every Wednesday", "Every Friday", "Every Sunday"]
NAMES = ["Alice", "Bob"]
HABITS = [
    ("Morning jog", "Jog for 30 minutes."),
    ("Read book", "Read at least 10 pages."),
    ("Meditate", "10 minutes meditation."),
    ("Go to gym", "Workout 1 hour."),
    ("Buy groceries", "Don't forget veggies."),
    ("Walk the dog", "Don't say it out loud."),
    ("Drink water", "At least 8 cups."),
    ("Journal", "Write a paragraph.")
]

def populate_all() -> None:
    """Creates interconnected dummy data."""
    print("CREATING DUMMY DATA")
    print("Dropping tables...")
    dbc.db_drop_all()
    print("Reinitializing db...")
    dbc.db_init()

    print("Creating users...")
    users = []
    for name in NAMES:
        username = name.lower()
        email = f"{username}@test.com"
        password = hashlib.sha256("password123".encode()).hexdigest()
        dbc.db_create_user(name, username, email, password)
        user_id = dbc.db_get_userid_by_credentials(username, password)
        users.append((user_id, name))

    print("Creating habits...")
    habit_ids = []
    for user_id, name in users:
        # Only add habits for Bob
        if name == "Bob":
            for habit_name, habit_desc in HABITS:
                habit_id = dbc.db_create_habit_data(
                    author_user_id=user_id,
                    author_display_name=name,
                    habit_name=habit_name,
                    habit_desc=habit_desc,
                    b_public=True,
                    b_official=False,
                    last_modified=datetime.now().isoformat()
                )
                habit_ids.append((habit_id, user_id))

    print("Subscribing users to habits...")
    subs = []
    for habit_id, user_id in habit_ids:
        periodicity = random.choice(PERIODICITIES)
        creation_date = (datetime.now() - timedelta(days=28)).date().isoformat()
        latest_date = datetime.now().date().isoformat()
        sub_id = dbc.db_create_habit_sub(
            owner_user_id=user_id,
            habit_data_id=habit_id,
            creation_date=creation_date,
            latest_date=latest_date,
            periodicity=periodicity,
            cur_streak=random.randint(1, 5),
            max_streak=random.randint(5, 10)
        )
        subs.append((sub_id, user_id, periodicity))

    print("Adding completions for the last 4 weeks...")
    cx = sqlite3.connect(dbc.Connection.FILE.value)
    today = datetime.now().date()
    for sub_id, user_id, periodicity in subs:
        for i in range(28):
            date = today - timedelta(days=i)
            if periodicity == "Daily" or (periodicity == "Weekly" and date.weekday() == 0) or \
               (periodicity == "Every Monday" and date.weekday() == 0) or \
               (periodicity == "Every Wednesday" and date.weekday() == 2) or \
               (periodicity == "Every Friday" and date.weekday() == 4) or \
               (periodicity == "Every Sunday" and date.weekday() == 6):
                if random.random() < 0.8:  # 80% chance of completion
                    cx.execute(
                        """
                        INSERT INTO completion (date, user_id, habit_sub_id)
                        VALUES (?, ?, ?)
                        """,
                        (date.isoformat(), user_id, sub_id)
                    )
    cx.commit()
    cx.close()

    print("FINISHED CREATING DUMMY DATA.")

if __name__ == "__main__":
    populate_all()