import random
import hashlib
from datetime import date, datetime, timedelta

import obj.src.subscription as sub
import db.src.controller as dbc


def populate_all() -> None:
    #  Init
    print("CREATING DUMMY DATA.")
    print("Dropping tables...")
    dbc.db_drop_all()
    print("Reinitializing db...")
    dbc.db_init()

    # User
    print("Creating Users...")
    pw=hashlib.sha256("password123".encode()).hexdigest()
    dbc.db_create_user("HTOfficial", "admin", "admind@ht.com", pw)
    dbc.db_create_user("Alice", "alice", "alice@test.com", pw)
    dbc.db_create_user("Bob", "bob", "bob@test.com", pw)

    # HabitData
    print("Creating Habits...")
    # 4 official
    dbc.db_create_habit_data(0, "HTOfficial", "Read book", "Read at least 10 pages.", True, True)
    dbc.db_create_habit_data(0, "HTOfficial", "Meditate", "10 minutes of meditation.", True, True)
    dbc.db_create_habit_data(0, "HTOfficial", "Workout", "30 minutes of exercising.", True, True)
    dbc.db_create_habit_data(0, "HTOfficial", "Journal", "Write a paragraph.", True, True)
    # 6 authored by Alice
    HABITS = [
        ("Morning jog", "Jog for 30 minutes."),
        ("Read book", "Read at least 10 pages."),
        ("Go to gym", "Workout 1 hour."),
        ("Buy groceries", "Don't forget veggies."),
        ("Walk the dog", "Don't say it out loud."),
        ("Drink water", "At least 6 cups."),
    ]
    for habit_name, habit_desc in HABITS:
        dbc.db_create_habit_data(
            author_user_id=1,
            author_display_name="Alice",
            habit_name=habit_name,
            habit_desc=habit_desc,
            b_public=random.choice([True, False]),
            b_official=False,
            last_modified=random.choice(["", datetime.today().isoformat()])
        )

    # HabitSubscriptions
    print("Creating Subscriptions & Completions...")
    # Sub 0 -> Monday, no completions
    dbc.db_create_habit_sub(2, 0, date.today().isoformat(), None, sub.Periodicity.MONDAY.value, 0, 0)
    # Sub 1 -> Tuesday, completed: 2w, 1w ago, streak : 2|2
    dbc.db_create_habit_sub(2, 1, date.today().isoformat(), get_previous_weekday(0, 1).isoformat(), sub.Periodicity.TUESDAY.value, 2, 2)
    dbc.db_create_completion(get_previous_weekday(1, 2).isoformat(), 1, 1)
    dbc.db_create_completion(get_previous_weekday(1, 1).isoformat(), 1, 1)
    # Sub 2 -> Wednesday, completed: 3w, 2w, 1w ago, streak: 3|3
    dbc.db_create_habit_sub(2, 2, date.today().isoformat(), get_previous_weekday(2, 1).isoformat(), sub.Periodicity.WEDNESDAY.value, 3, 3)
    dbc.db_create_completion(get_previous_weekday(2, 3).isoformat(), 1, 2)
    dbc.db_create_completion(get_previous_weekday(2, 2).isoformat(), 1, 2)
    dbc.db_create_completion(get_previous_weekday(2, 1).isoformat(), 1, 2)
    # Sub 3 -> Thursday, completed: 1w ago, streak: 1|1
    dbc.db_create_habit_sub(2, 3, date.today().isoformat(), get_previous_weekday(3, 1).isoformat(), sub.Periodicity.THURSDAY.value, 1, 1)
    dbc.db_create_completion(get_previous_weekday(3, 1).isoformat(), 1, 3)
    # Sub 4 -> Friday, completed: 2w ago, streak: 0|1
    dbc.db_create_habit_sub(2, 4, date.today().isoformat(), get_previous_weekday(4, 2).isoformat(), sub.Periodicity.FRIDAY.value, 0, 1)
    dbc.db_create_completion(get_previous_weekday(4, 2).isoformat(), 1, 4)
    # Sub 5 -> Saturday, completed: 3w ago, streak: 0|1
    dbc.db_create_habit_sub(2, 5, date.today().isoformat(), get_previous_weekday(5, 3).isoformat(), sub.Periodicity.SATURDAY.value, 0, 1)
    dbc.db_create_completion(get_previous_weekday(5, 3).isoformat(), 1, 5)
    # Sub 6 -> Sunday, completed: 3w, 2w ago, streak: 0|2
    dbc.db_create_habit_sub(2, 6, date.today().isoformat(), get_previous_weekday(6, 2).isoformat(), sub.Periodicity.SUNDAY.value, 0, 2)
    dbc.db_create_completion(get_previous_weekday(6, 2).isoformat(), 1, 6)
    dbc.db_create_completion(get_previous_weekday(6, 3).isoformat(), 1, 6)
    # Sub 7 -> Daily, completed: last 5 days, excl. today, streak: 5|5
    dbc.db_create_habit_sub(2, 7, date.today().isoformat(), date.today().isoformat(), sub.Periodicity.DAILY.value, 5, 5)
    for i in range(1, 6):
        dbc.db_create_completion((date.today() - timedelta(days=i)).isoformat(), 1, 7)
    # Sub 8 -> Daily, completed: 12 days, then 3 days break, 3 days, then 5 days break, then 2 days incl. today, streak: 2|4
    dbc.db_create_habit_sub(2, 8, date.today().isoformat(), date.today().isoformat(), sub.Periodicity.DAILY.value, 2, 4)
    for i in range(12+3+3+5+2):
        if (i >= 2 and i < 7) or (i >= 10 and i < 13): # break 1 & 2
            continue
        dbc.db_create_completion((date.today() - timedelta(days=i)).isoformat(), 1, 8)
    # Sub 9 -> Weekly, completed: today, last 3 sundays, streak: 4|4
    dbc.db_create_habit_sub(2, 9, date.today().isoformat(), date.today().isoformat(), sub.Periodicity.WEEKLY.value, 4, 4)
    dbc.db_create_completion(get_previous_weekday(6, 3).isoformat(), 1, 9)
    dbc.db_create_completion(get_previous_weekday(6, 2).isoformat(), 1, 9)
    dbc.db_create_completion(get_previous_weekday(6, 1).isoformat(), 1, 9)

    print("FINISHED CREATING DEBUG DUMMY DATA.")
    print("Login using username: \"alice\" or \"bob\" and password: \"password123\".")
    print("Bob is an empty test account, while the alice account contains dummy data.")

def get_previous_weekday(target_weekday:int, weeks_ago:int=1) -> date:
    """Returns the date of the `weeks_ago`-th previous occurrence of the target weekday.
    Helper function.

    Args:
        target_weekday (int): Monday = 0, Sunday = 6.
        weeks_ago (int): 1 for last week, 2 for 2nd last, etc.

    Returns:
        date: The date of the desired past weekday.
    """
    today = date.today()
    today_weekday = today.weekday()
    days_since_target = (today_weekday - target_weekday) % 7 + 7 * (weeks_ago - 1)
    return today - timedelta(days=days_since_target)

if __name__ == "__main__":
    populate_all()