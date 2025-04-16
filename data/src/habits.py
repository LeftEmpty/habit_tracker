import datetime
from dataclasses import dataclass


@dataclass
class Periodicty:
    # Timeframe (in hours)
    timeframe: int
    # Frequency (in hours)
    frequency: int


class HabitData:
    def __init__(self, habit_id:int, name:str, desc:str):
        """"""
        self.habit_id:int = habit_id
        self.name:str = name
        self.desc:str = desc


class HabitSubscription:
    def __init__(self, userhabit_id, user_id, habit_id, start_date,
                    last_completed_date, periodicty, cur_streak, max_streak):
        """The habit itself is defined via the HabitData class (see above).
        This class intends to couple the User and the Habit together, such that
        Habits can be reused by multiple users while retaining individual progress"""
        self.start_date = start_date
        self.last_completed_date = last_completed_date
        self.periodicty = periodicty
        self.cur_streak = cur_streak
        self.max_streak = max_streak