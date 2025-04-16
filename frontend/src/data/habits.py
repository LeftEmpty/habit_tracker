from datetime import date, timedelta
from dataclasses import dataclass
from enum import Enum


class Periodicty(Enum):
    DAILY = "Daily" # once a day, every day
    WEEKLY = "Weekly" # once a week, every week
    MONDAY = "Every Monday" # every week, on monday
    TUESDAY = "Every Tuesday" # "..
    WEDNESDAY = "Every Wednesday"
    THURSDAY = "Every Thursday"
    FRIDAY = "Every Friday"
    SATURDAY = "Every Saturday"
    SUNDAY = "Every Sunday"

@dataclass
class HabitData:
    def __init__(self, habit_id:int, name:str, desc:str):
        """Data class for keeping track of habit data, should reflect the respecive db entry

        Args:
            habit_id (int): _description_
            name (str): _description_
            desc (str): _description_
        """
        self.habit_id:int = habit_id
        self.name:str = name
        self.desc:str = desc


@dataclass
class Completion:
    def __init__(self, completion_id:int, user_id:int, habit_sub_id:int, date:str):
        """Data class for keeping track of habit completions, should reflect the respecive db entry

        Args:
            completion_id (int): _description_
            user_id (int): _description_
            habit_sub_id (int): _description_
            date (str): _description_
        """
        self.completion_id:int = completion_id
        self.habit_sub_id:int = habit_sub_id
        self.user_id:int = user_id
        self.date:str = date


class HabitSubscription:
    def __init__(self, habit_sub_id:int, user_id:int, habit_id:int, start_date:date,
                    last_completed_date:date, periodicty:Periodicty, cur_streak:int, max_streak:int):
        """The habit itself is defined via the HabitData class (see above).
        This class intends to couple the User and the Habit together, such that
        Habits can be reused by multiple users while retaining individual progress

        Args:
            habit_sub_id (int): _description_
            user_id (int): _description_
            habit_id (int): _description_
            start_date (date): _description_
            last_completed_date (date): _description_
            periodicty (Periodicty): _description_
            cur_streak (int): _description_
            max_streak (int): _description_
        """
        self.habit_sub_id:int = habit_sub_id
        self.start_date = start_date
        self.last_completed_date = last_completed_date
        self.periodicty:Periodicty = periodicty
        self.cur_streak:int = cur_streak
        self.max_streak:int = max_streak

        self.habit_data:HabitData # @TODO get_habit_data(habit_id)

        self.is_completed = self.get_completed_state()


    def get_completed_state(self) -> bool:
        """Check if the last completion of this habit (that is due today)
        already happened within the period that was allocated to it
        (used to for example draw habit-widget as 'checked-off' in gui)

        Raises:
            ValueError: May raise a ValueError if current periodicity is invalid

        Returns:
            bool: True if already completed
        """
        today = date.today()
        weekday_map = {
            Periodicty.MONDAY: 0,
            Periodicty.TUESDAY: 1,
            Periodicty.WEDNESDAY: 2,
            Periodicty.THURSDAY: 3,
            Periodicty.FRIDAY: 4,
            Periodicty.SATURDAY: 5,
            Periodicty.SUNDAY: 6,
        }
        # every wednesday / daily -> have we completed it today?
        if self.periodicty == Periodicty.DAILY or self.periodicty in weekday_map:
            end_date = today
        # weekly -> have we completed it since monday? #// weekly -> did we complete at any time during the last 7 days
        elif self.periodicty == Periodicty.WEEKLY:
            end_date = today - timedelta(days=((today.weekday() - weekday_map[self.periodicty]) % 7)) # gets date of current week's monday
        else:
            raise ValueError(f"Unsupported periodicity: {self.periodicty}")
        return not len(self.get_completions_for_period(today, end_date)) > 0


    def add_completion_event(self, date:date = date.today()) -> None:
        """Add a completion entry for this user & subscription

        Args:
            date (date, optional): date on which the completion event occured. Defaults to date.today().
        """
        if self.is_completed : return
        #@TODO

    def get_completions_for_period(self, start_date:date, end_date:date) -> list[Completion]:
        """returns all completion events for the given habit_subscription"""

        # return sqlcontroller.get_entries_for_period(day_count, int)
        return []