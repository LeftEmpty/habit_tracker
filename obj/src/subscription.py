from datetime import date, timedelta
from dataclasses import dataclass
from enum import Enum

import obj.util.request_handler as request

# forward declaring for better overview
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from obj.src.habit import HabitData

class Periodicity(Enum):
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
    def __init__(self, user_id:int, data_id:int, periodicity:Periodicity|str, cur_streak:int, max_streak:int,
        last_completed_date:date|None, creation_date:date = date.today(), habit_data:Optional["HabitData"]=None, sub_id:int = -2):
        """The habit itself is defined via the HabitData class (see above).
        This class intends to couple the User and the Habit together, such that
        Habits can be reused by multiple users while retaining individual progress.

        Args:
            user_id (int): _description_
            habit_id (int): _description_
            periodicity (Periodicity | str): _description_
            cur_streak (int): _description_
            max_streak (int): _description_
            last_completed_date (date | None): _description_
            creation_date (date, optional): _description_. Defaults to date.today().
            habit_data (Optional[&quot;HabitData&quot;], optional): _description_. Defaults to None.
            sub_id (int, optional): _description_. Defaults to -2.
        """
        self.id:int = sub_id
        self.data_id:int = data_id
        self.owner_id:int = user_id
        self.creation_date:date = creation_date
        self.last_completed_date:date|None = last_completed_date
        self.periodicity:Periodicity = self._normalize_periodicity(periodicity)
        self.cur_streak:int = cur_streak
        self.max_streak:int = max_streak

        self.completed_locally:bool = self.get_completed_state()

        # try get habit data if it isn't provided
        if habit_data:
            self.habit_data = habit_data
        else:
            data = request.get_habit_data(self.data_id)
            if data:
                self.habit_data:HabitData = data

        # register self to database (will just get id if already in db)
        if self.id < 0:
            self.register_self()

    def register_self(self) -> int:
        """Saves itself (this habit sub) to the database.
        May not create a new entry if data is missing or an identical entry is found.

        Returns:
            int: returns the ID of the habit subcription entry, ERROR CODE: -1"""
        # validate data
        if not self.is_complete(): return -1

        # already registered
        if self.id > 0: return self.id

        # create habit_data entry in table get resulting self.id -> Error code is -1
        new_id = request.create_new_sub_for_user(self.owner_id, self)
        if new_id > 0:
            self.id = new_id
            return new_id
        else:
            return -1

    def is_complete(self) -> bool:
        """Checks that all dada required to register has been set

        Returns:
            bool: False if any of the data is None/empty, True if all have been set
        """
        if self.data_id is None or self.data_id < 0: return False
        if self.owner_id is None or self.owner_id < 0: return False
        return True

    def is_registered(self) -> bool:
        """Returns true if subscription has been registered properly, i.e. if this object reflects an entry in DB.
        This is done by checking if the data object has a valid ID

        Returns:
            bool: returns ID >= 0 (-2 is default when unset)
        """
        return self.id >= 0

    def __bool__(self) -> bool:
        return self.id is not None and self.id >= 0

    def _normalize_periodicity(self, value: str | Periodicity) -> Periodicity:
        if isinstance(value, Periodicity):
            return value
        elif isinstance(value, str):
            try:
                # Match by enum value
                return Periodicity(value)
            except ValueError:
                raise ValueError(f"Invalid periodicity string: {value}")
        else:
            raise TypeError(f"Expected str or Periodicity, got {type(value)}")

    def get_completed_state(self) -> bool:
        """'Algorithm' to figure out if the subscription has been completed,
        according to the habits periodicity."""
        today = date.today()

        weekday_map = {
            Periodicity.MONDAY: 0,
            Periodicity.TUESDAY: 1,
            Periodicity.WEDNESDAY: 2,
            Periodicity.THURSDAY: 3,
            Periodicity.FRIDAY: 4,
            Periodicity.SATURDAY: 5,
            Periodicity.SUNDAY: 6,
        }

        if self.periodicity == Periodicity.DAILY:
            start_date = today
        elif self.periodicity == Periodicity.WEEKLY:
            start_date = today - timedelta(days=6)
        elif self.periodicity in weekday_map:
            if today.weekday() != weekday_map[self.periodicity]:
                return False
            start_date = today
        else:
            raise ValueError(f"Unsupported periodicity: {self.periodicity}")

        completions = self.get_completions_for_period(start_date, today)
        return len(completions) > 0

    def get_completed_state_old(self) -> bool:
        """Check if the last completion of this habit - that is due today -
        already happened within the period that was allocated to it.
        used to for example draw habit-widget as 'checked-off' in gui

        Raises:
            ValueError: May raise a ValueError if current periodicity is invalid

        Returns:
            bool: True if already completed
        """
        today = date.today()
        weekday_map = {
            Periodicity.MONDAY: 0,
            Periodicity.TUESDAY: 1,
            Periodicity.WEDNESDAY: 2,
            Periodicity.THURSDAY: 3,
            Periodicity.FRIDAY: 4,
            Periodicity.SATURDAY: 5,
            Periodicity.SUNDAY: 6,
        }
        # every wednesday / daily -> have we completed it today?
        if self.periodicity == Periodicity.DAILY or self.periodicity in weekday_map:
            end_date = today
        # weekly -> have we completed it since monday? #// weekly -> did we complete at any time during the last 7 days
        elif self.periodicity == Periodicity.WEEKLY:
            end_date = today - timedelta(days=((today.weekday() - weekday_map[self.periodicity]) % 7)) # gets date of current week's monday
        else:
            raise ValueError(f"Unsupported periodicity: {self.periodicity}")
        return not len(self.get_completions_for_period(today, end_date)) > 0

    def add_completion_event(self, date:date = date.today()) -> None:
        """Add a completion entry for this user & subscription

        Args:
            date (date, optional): date on which the completion event occured. Defaults to date.today().
        """
        if self.get_completed_state(): return
        # CompletionEvent()
        # @TODO might be good to let user's properly un-check / 'un-complete' their habits - delete completion entry & reset locally


    def get_completions_for_period(self, start_date:date, end_date:date) -> list[Completion]:
        """returns all completion events for the given habit_subscription"""
        # @TODO
        return []

    def on_cancel_subscription(self) -> None:
        """Event that should be called when a user cancels this subscription,
        when the user was the last subscriber to the used habit, then also delete that habit (only unofficial)"""
        pass