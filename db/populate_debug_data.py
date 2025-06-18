import random
import hashlib
from datetime import date, datetime, timedelta

import obj.subscription as sub
import db.controller as dbc


def populate_all(conn:dbc.Connection=dbc.Connection.FILE) -> None:
    #  Init
    if conn != dbc.Connection.TEST: print("------- CREATING DUMMY DATA. -------")
    if conn != dbc.Connection.TEST: print("Dropping tables...")
    dbc.db_drop_all(conn)
    if conn != dbc.Connection.TEST: print(f"Reinitializing db on connection: {conn}...")
    dbc.db_init(conn)

    # User
    if conn != dbc.Connection.TEST: print("Creating Users...")
    pw=hashlib.sha256("password123".encode()).hexdigest()
    dbc.db_create_user("HTOfficial", "admin", "admind@ht.com", pw, conn)
    dbc.db_create_user("Alice", "alice", "alice@test.com", pw, conn)
    dbc.db_create_user("Bob", "bob", "bob@test.com", pw, conn)

    # HabitData
    if conn != dbc.Connection.TEST: print("Creating Habits...")
    # 4 official
    dbc.db_create_habit_data(1, "HTOfficial", "Read book", "Read at least 10 pages.", True, True, conn=conn)
    dbc.db_create_habit_data(1, "HTOfficial", "Meditate", "10 minutes of meditation.", True, True, conn=conn)
    dbc.db_create_habit_data(1, "HTOfficial", "Workout", "30 minutes of exercising.", True, True, conn=conn)
    dbc.db_create_habit_data(1, "HTOfficial", "Journal", "Write a paragraph.", True, True, conn=conn)
    # 6 authored by Alice
    HABITS = [
        ("Morning jog", "Jog for 30 minutes."),
        ("Read book", "Read at least 10 pages."),
        ("Go to gym", "Workout 1 hour."),
        ("Buy groceries", "Don't forget veggies."),
        ("Walk the dog", "Don't say it out loud."),
        ("Drink water", "At least 6 cups."),
    ]
    for i, (habit_name, habit_desc) in enumerate(HABITS):
        dbc.db_create_habit_data(
            author_user_id=2,
            author_display_name="Alice",
            habit_name=habit_name,
            habit_desc=habit_desc,
            b_public=(i % 2 == 0),
            b_official=False,
            last_modified=random.choice(["", datetime.today().isoformat()]),
            conn=conn
        )
    # 2 public / 1 private by bob
    dbc.db_create_habit_data(3, "Bob", "Bob's Habit 1", "Public test habit.", True, False, conn=conn)
    dbc.db_create_habit_data(3, "Bob", "Bob's Habit 2", "Public test habit with a longer descrpition.", True, False, conn=conn)
    dbc.db_create_habit_data(3, "Bob", "Bob's Habit 3", "'Private' test habit.", False, False, conn=conn)

    # HabitSubscriptions
    if conn != dbc.Connection.TEST: print("Creating Subscriptions & Completions...")
    # Sub 1 -> Monday, no completions
    dbc.db_create_habit_sub(2, 1, date.today().isoformat(), None, sub.Periodicity.MONDAY.value, 0, 0, conn=conn)
    # Sub 2 -> Tuesday, completed: 2w, 1w ago, streak : 2|2 - creation date can be massively different
    dbc.db_create_habit_sub(2, 2, get_previous_weekday(1, 4).isoformat(), get_previous_weekday(0, 1).isoformat(), sub.Periodicity.TUESDAY.value, 2, 2, conn=conn)
    dbc.db_create_completion(get_previous_weekday(1, 2).isoformat(), 2, 2, conn=conn)
    dbc.db_create_completion(get_previous_weekday(1, 1).isoformat(), 2, 2, conn=conn)
    # Sub 3 -> Wednesday, completed: 3w, 2w, 1w ago, streak: 3|3
    dbc.db_create_habit_sub(2, 3, get_previous_weekday(2, 3).isoformat(), get_previous_weekday(2, 1).isoformat(), sub.Periodicity.WEDNESDAY.value, 3, 3, conn=conn)
    dbc.db_create_completion(get_previous_weekday(2, 3).isoformat(), 2, 3, conn=conn)
    dbc.db_create_completion(get_previous_weekday(2, 2).isoformat(), 2, 3, conn=conn)
    dbc.db_create_completion(get_previous_weekday(2, 1).isoformat(), 2, 3, conn=conn)
    # Sub 4 -> Thursday, completed: 1w ago, streak: 1|1
    dbc.db_create_habit_sub(2, 4, get_previous_weekday(3, 1).isoformat(), get_previous_weekday(3, 1).isoformat(), sub.Periodicity.THURSDAY.value, 1, 1, conn=conn)
    dbc.db_create_completion(get_previous_weekday(3, 1).isoformat(), 2, 4, conn=conn)
    # Sub 5 -> Friday, completed: 2w ago, streak: 0|1
    dbc.db_create_habit_sub(2, 5, get_previous_weekday(4, 2).isoformat(), get_previous_weekday(4, 2).isoformat(), sub.Periodicity.FRIDAY.value, 0, 1, conn=conn)
    dbc.db_create_completion(get_previous_weekday(4, 2).isoformat(), 2, 5, conn=conn)
    # Sub 6 -> Saturday, completed: 3w ago, streak: 0|1
    dbc.db_create_habit_sub(2, 6, get_previous_weekday(5, 3).isoformat(), get_previous_weekday(5, 3).isoformat(), sub.Periodicity.SATURDAY.value, 0, 1, conn=conn)
    dbc.db_create_completion(get_previous_weekday(5, 3).isoformat(), 2, 6, conn=conn)
    # Sub 7 -> Sunday, completed: 3w, 2w ago, streak: 0|2 - creation date can be different than periodicity weekday
    dbc.db_create_habit_sub(2, 7, get_previous_weekday(4, 3).isoformat(), get_previous_weekday(6, 2).isoformat(), sub.Periodicity.SUNDAY.value, 0, 2, conn=conn)
    dbc.db_create_completion(get_previous_weekday(6, 2).isoformat(), 2, 7, conn=conn)
    dbc.db_create_completion(get_previous_weekday(6, 3).isoformat(), 2, 7, conn=conn)
    # Sub 8 -> Daily, completed: last 5 days, excl. today, streak: 5|5
    dbc.db_create_habit_sub(2, 8, (date.today() - timedelta(days=5)).isoformat(), (date.today() - timedelta(days=1)).isoformat(), sub.Periodicity.DAILY.value, 5, 5, conn=conn)
    for i in range(1, 6):
        dbc.db_create_completion((date.today() - timedelta(days=i)).isoformat(), 2, 8, conn=conn)
    # Sub 9 -> Daily, completed: 12 days, then 3 days break, 3 days, then 5 days break, then 2 days incl. today, streak: 2|4
    dbc.db_create_habit_sub(2, 9, (date.today() - timedelta(days=12+3+3+5+2)).isoformat(), date.today().isoformat(), sub.Periodicity.DAILY.value, 2, 4, conn=conn)
    for i in range(12+3+3+5+2):
        if (i >= 2 and i < 7) or (i >= 10 and i < 13): # break 1 & 2
            continue
        dbc.db_create_completion((date.today() - timedelta(days=i)).isoformat(), 2, 9, conn=conn)
    # Sub 10 -> Weekly, completed: today, last 3 sundays, streak: 4|4
    dbc.db_create_habit_sub(2, 10, get_previous_weekday(6, 1).isoformat(), date.today().isoformat(), sub.Periodicity.WEEKLY.value, 4, 4, conn=conn)
    dbc.db_create_completion(date.today().isoformat(), user_id=1, habit_sub_id=4, conn=conn)
    dbc.db_create_completion(get_previous_weekday(6, 3).isoformat(), 2, 10, conn=conn)
    dbc.db_create_completion(get_previous_weekday(6, 2).isoformat(), 2, 10, conn=conn)
    dbc.db_create_completion(get_previous_weekday(6, 1).isoformat(), 2, 10, conn=conn)

    # Sub 11 (Bob) -> Daily, completed: last 5 days, excl. today, streak: 5|5
    dbc.db_create_habit_sub(3, 11, (date.today() - timedelta(days=5)).isoformat(), (date.today() - timedelta(days=1)).isoformat(), sub.Periodicity.DAILY.value, 5, 5, conn=conn)
    for i in range(1, 6):
        dbc.db_create_completion((date.today() - timedelta(days=i)).isoformat(), 3, 11, conn=conn)
    # Sub 12 (Bob) -> Daily, completed: last 6 days, incl. today, streak: 7|7
    dbc.db_create_habit_sub(3, 12, (date.today() - timedelta(days=7)).isoformat(), (date.today()).isoformat(), sub.Periodicity.DAILY.value, 7, 7, conn=conn)
    for i in range(7):
        dbc.db_create_completion((date.today() - timedelta(days=i)).isoformat(), 3, 12, conn=conn)
    # Sub 13 (Bob) -> Daily, completed: 15 days, 5 days break
    dbc.db_create_habit_sub(3, 13, (date.today() - timedelta(days=15+5)).isoformat(), (date.today() - timedelta(days=5)).isoformat(), sub.Periodicity.DAILY.value, 0, 15, conn=conn)
    for i in range(15+5):
        if (i < 5): # 5 day break
            continue
        dbc.db_create_completion((date.today() - timedelta(days=i)).isoformat(), 3, 13, conn=conn)

    if conn != dbc.Connection.TEST: print("------- FINISHED CREATING DEBUG DUMMY DATA. -------")
    if conn != dbc.Connection.TEST: print("Login using username: \"alice\" or \"bob\" and password: \"password123\".")

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
    populate_all(conn=dbc.Connection.FILE)