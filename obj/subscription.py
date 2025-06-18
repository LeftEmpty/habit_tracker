from datetime import datetime, date, timedelta
from dataclasses import dataclass
from enum import Enum

import obj.request_handler as request
from db.controller import Connection

# forward declaring for better overview
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from obj.habit import HabitData


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

    def weekday_index(self) -> int:
        """Returns the 0-based index of the weekday if this is a weekday periodicity.

        Returns:
            int: 0 (Monday) through 6 (Sunday)

        Raises:
            ValueError: If the periodicity is not a weekday.
        """
        weekday_map = {
            Periodicity.MONDAY: 0,
            Periodicity.TUESDAY: 1,
            Periodicity.WEDNESDAY: 2,
            Periodicity.THURSDAY: 3,
            Periodicity.FRIDAY: 4,
            Periodicity.SATURDAY: 5,
            Periodicity.SUNDAY: 6
        }
        if self not in weekday_map:
            raise ValueError(f"Periodicity '{self.value}' is not a specific weekday.")
        return weekday_map[self]


@dataclass
class Completion:
    def __init__(self, user_id:int, habit_sub_id:int, compl_date:date):
        """Data class for keeping track of habit completions, should reflect the respecive db entry

        Args:
            completion_id (int): _description_
            user_id (int): _description_
            habit_sub_id (int): _description_
            date (str): _description_
        """
        self.habit_sub_id:int = habit_sub_id
        self.user_id:int = user_id
        self.compl_date:date = compl_date


class HabitSubscription:
    def __init__(self, user_id:int, data_id:int, periodicity:Periodicity|str, cur_streak:int, max_streak:int,
        last_completed_date:date|None, creation_date:date=date.today(), habit_data:Optional["HabitData"]=None, sub_id:int=-2):
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
        cd:date|None = self._normalize_date(creation_date)
        if cd:
            self.creation_date:date = cd
        self.last_completed_date:date|None = last_completed_date
        if last_completed_date != None:
            self.last_completed_date = self._normalize_date(last_completed_date)
        self.periodicity:Periodicity = self._normalize_periodicity(periodicity)
        self.cur_streak:int = cur_streak
        self.max_streak:int = max_streak

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
        if not self.is_data_complete(): return -1

        # already registered
        if self.id > 0: return self.id

        # create habit_data entry in table get resulting self.id -> Error code is -1
        new_id = request.create_new_sub_for_user(self.owner_id, self)
        if new_id > 0:
            self.id = new_id
            return new_id
        else:
            return -1

    def is_data_complete(self) -> bool:
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
        """Normalize a periodicity, i.e. can take a periodicity OR string and return a periodicity enum.

        @TODO This should arguably be a global helper function instead of being in this class.

        Args:
            value (str | Periodicity): periodicity to normalize, may be a string or enum.

        Raises:
            ValueError: Invalid periodicity string, string is not part of Enum.
            TypeError: Expected str or Periodicity, value input has wrong Type.

        Returns:
            Periodicity: Enum variable associated with the value input.
        """
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

    def _normalize_date(self, d:date|str) -> date|None:
        """Simplified date normalization. Returns date object matching the input value.

        Args:
            d (date | str): Input value, may be string or date object.

        Returns:
            date|None: date variable associated with the input. May Return None.
        """
        if isinstance(d, date):
            return d
        if d == "":
            return None
        dt = datetime.strptime(d, "%Y-%m-%d").date()
        return dt

    def _periodicty_relevant_today(self) -> bool:
        """Checks if subscription's periodicity weekday is same as todays, which makes it relevant.
        Daily or Weekly subscriptions are always relevant."""
        if self.periodicity == Periodicity.DAILY or self.periodicity == Periodicity.WEEKLY or\
            self.periodicity.weekday_index() == date.today().weekday():
            return True
        else:
            return False

    def on_completion_input_action(self) -> None:
        """Gets input to change completion state, essentially a toggle function which checks current state and validates input semantic."""
        # Get current state
        cur_compl:bool = self.get_completed_state()
        if cur_compl:
            self._retract_completion_event()
        else:
            self._add_completion_event()

    def get_completed_state(self, last_completion:Optional[Completion]=None) -> bool:
        """'Algorithm' to figure out if the subscription has been completed.
        Checks if one of this subs completions has a date in the current periodicity timeframe.

        Args:
            completions (list[Completion], optional): Can provide completions if assumed to be correct to reduce query load. Defaults to [].

        Returns:
            bool: sub is currently completed.
        """
        latest_compl = request.get_latest_sub_completion_for_user(self.owner_id, self.id)
        if last_completion != None:
            latest_compl = last_completion
        if not latest_compl:
            print(f"No completion found for sub with id|habit {self.id}|{self.habit_data.name} from user {self.owner_id}.")
            return False

        check_date:date = latest_compl.compl_date
        today:date = date.today()

        # Completed if daily and already completetd today
        if self.periodicity == Periodicity.DAILY and check_date == today:
            return True
        # Completed if weekly and completed since this weeks monday
        elif self.periodicity == Periodicity.WEEKLY and check_date >= today - timedelta(days=today.weekday()):
            return True
        # Completed if last same weekday and last completion was today, last weekday doesn't count.. *(not daily/weekly so we can check index)
        elif self.periodicity != Periodicity.WEEKLY and self.periodicity != Periodicity.DAILY and\
            self.periodicity.weekday_index() == today.weekday() and check_date == today:
            return True
        # False otherwise..
        else:
            return False

    def _add_completion_event(self, compl_date:date=date.today()) -> None:
        """Add a completion entry for this user & subscription.
        Update self on successful completion event, update last completion date & streaks.

        Args:
            date (date, optional): date on which the completion event occured. Defaults to date.today().

        Returns:
            bool: success / failure
        """
        if request.create_completion(Completion(self.owner_id, self.id, compl_date)):
            self.last_completed_date = compl_date
            self.cur_streak += 1
            if self.cur_streak > self.max_streak:
                self.max_streak = self.cur_streak

            #? could implement some sort of habit finished or goal reached functionality here

            request.update_sub_entry(self)

    def _retract_completion_event(self) -> None:
        """Gets the latest completion and deletes db entry if applicable.
        Also updatesm last completion date to previous completion or none & updates streaks (clamp min 0)."""
        latest:Completion|None = request.get_latest_sub_completion_for_user(self.owner_id, self.id)
        if latest:
            if request.delete_completion(self.owner_id, self.id, latest.compl_date):
                new_latest:Completion|None = request.get_latest_sub_completion_for_user(self.owner_id, self.id)
                if new_latest:
                    self.last_completed_date = new_latest.compl_date
                    self.cur_streak -= 1
                    if self.cur_streak < 0:
                        self.cur_streak = 0
                else:
                    self.last_completed_date = None
                    self.cur_streak = self.max_streak = 0
                request.update_sub_entry(self)

    def get_sub_completions(self, b_all:bool=True, start_date:date=date.today(), end_date:date=date.today(), b_test:bool=False) -> list[Completion]:
        """Get all completions for this subscription (and it's owning user).
        Toggable by bool to specify a timeframe via start/end date parameters.

        Args:
            b_all (bool, optional): Return all completions. Defaults to True.
            start_date (date, optional): start of timeframe, requires b_all=False. Defaults to date.today().
            end_date (date, optional): end of timeframe, requires b_all=False. Defaults to date.today().

        Returns:
            list[Completion]: list of all completions.
        """
        if b_all:
            completions = request.get_all_sub_completions_for_user(self.owner_id, self.id) if not b_test\
                        else request.get_all_sub_completions_for_user(self.owner_id, self.id, Connection.TEST)
            if not len(completions) > 0: return []
            else: return completions
        elif not b_all and start_date and end_date and start_date < end_date:
            # @TODO
            return []

        print(f"Error getting sub completions due to improper function usage - check the dates.")
        return []

    def get_completion_rate(self, b_test:bool=False) -> tuple[int, int, float]:
        """Figures out success/completion rate by how often the sub should have been completed
        and how many times it actually was.

        Args:
            b_test (bool, optional): _description_. Defaults to False.

        Returns:
            tuple[int, int, float]: (done, expected, percentage)
        """
        start_date:date = self.creation_date
        end_date:date = date.today()
        delta_days = (end_date - start_date).days + 1  # include today

        # Get completions
        completions = self.get_sub_completions(b_test=b_test)
        actual_count = len(completions)

        # Calculate expected completions
        if self.periodicity == Periodicity.DAILY:
            expected_count = delta_days
        elif self.periodicity == Periodicity.WEEKLY:
            # full 7 day weeks + potential partial week
            expected_count = (delta_days // 7) + (1 if delta_days % 7 else 0)
        else:
            # counts occurences of the weekday, done by comparing the weekday to periodicity weekday index for every day in timespan
            weekday_index = self.periodicity.weekday_index()
            expected_count = sum(1 for i in range(delta_days)
                                if (start_date + timedelta(days=i)).weekday() == weekday_index)

        if expected_count == 0: # no divided by 0 errors in this house.
            return (0, 0, 0.0)

        rate = (actual_count / expected_count) * 100
        return (actual_count, expected_count, round(min(rate, 100.0), 2))

    def on_cancel_subscription(self) -> None:
        """Event that should be called when a user cancels this subscription,
        When the user was the last subscriber to the used habit (data), then also delete that habit (only unofficial)"""
        # delete sub and all completions for it
        request.delete_habit_sub(self.id)
        request.delete_all_sub_completions_for_user(self.owner_id, self.id)

        sub_count:int = self.habit_data.get_subscriber_count()

        # check habit data deletion rules
        if self.habit_data.author_id != self.owner_id:
            if sub_count > 0:
                print("can't delete habit data because user is not the author and habit is still subscribed to by someone else.")
                return
            else:
                print("deleting habit data, author has unsubbed. current user is last subscriber.")
        else:
            if self.habit_data.b_public and sub_count > 0:
                print(f"can't delete habit data, we're author but it's public and still has other subscribers, ('{sub_count}' subbed users).")
                # @TODO - could rename habt data author_name to something like "[delted]".
                return

        request.delete_habit_data(self.data_id)

    def check_streak_broken(self, b_test:bool=False) -> bool:
        """Checks if current streak is broken, i.e. should be reset and does so when applicable.

        Args:
            b_test (bool, optional): Only used (i.e. set to True) when unit testing. Defaults to False.

        Returns:
            bool: True if broken, False if still 'intact'
        """
        today = date.today()
        expected_latest:date

        if not self.last_completed_date:
            if self.cur_streak != 0:
                self.cur_streak = 0
                if not b_test: request.update_sub_entry(self)
                return True

        else:
            # DAILY - Broken if last completed more than 1 day ago
            if self.periodicity == Periodicity.DAILY:
                expected_latest:date = today - timedelta(days=1)
            # WEEKLY - Broken if last completed 2 weeks ago (i.e. last week + currently started week)
            elif self.periodicity == Periodicity.WEEKLY:
                expected_latest = today - timedelta(days=7 + today.weekday())
            # WEEKDAY - Broken if last completed longer than last weekday ago (i.e. 8)
            else:
                expected_latest = today - timedelta(days=7)

            if self.last_completed_date < expected_latest:
                if not b_test: print(f"Streak broken on sub [id:{self.id}|({self.habit_data.name})]")
                self.cur_streak = 0
                if not b_test: request.update_sub_entry(self)
                return True

        return False

    def modify_sub(self, periodicity:Periodicity|str) -> None:
        """Modifies this subs data & modifies entry in db"""
        p = self._normalize_periodicity(periodicity)
        self.periodicity = p
        request.update_sub_entry(self)