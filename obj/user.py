from obj.habit import HabitData
from obj.subscription import HabitSubscription
from gui.util.gui_enums import HabitQueryCondition
import obj.request_handler as request

from datetime import date, timedelta


class User:
    def __init__(self, user_id:int, display_name:str, username:str, email:str, subs:list[HabitSubscription] = list()):
        """User class for this project. Set in base GUI class.

        intentionally not saving password to this obj for obvious reasons.

        Args:
            user_id (int): _description_
            display_name (str): _description_
            username (str): _description_
            email (str): _description_
            habits (set[HabitSubscription], optional): list of subs the user 'owns'. Defaults to list().
        """
        self.user_id:int = user_id
        self.display_name:str = display_name
        self.email:str = email
        self.username = username
        self.habit_subs:list[HabitSubscription] = subs

        if len(self.habit_subs) == 0:
            self.habit_subs = self.get_subscribed_habits(HabitQueryCondition.ALL)

        self.init_complete = True

    def __bool__(self):
        return self.user_id is not None and self.user_id >= 0

    def get_subscribed_habits(self, cond:HabitQueryCondition=HabitQueryCondition.ALL) -> list[HabitSubscription]:
        """_summary_

        Args:
            cond (HabitQuerryCondition): _description_

        Returns:
            list[HabitSubscription]: _description_
        """
        if cond == HabitQueryCondition.NONE:
            return []

        subs:list[HabitSubscription] = request.get_subs_for_user(self.user_id)
        result:list[HabitSubscription] = []

        if cond == HabitQueryCondition.ALL:
            return subs
        if cond == HabitQueryCondition.RELEVANT_TODAY:
            for s in subs:
                if s._periodicty_relevant_today():
                    result.append(s)
        if cond == HabitQueryCondition.DUE:
            for s in subs:
                if not s.get_completed_state():
                    result.append(s)
        if cond == HabitQueryCondition.COMPLETED:
            for s in subs:
                if s.get_completed_state():
                    result.append(s)
        return result

    def update_subscribed_habits(self) -> None:
        """Simply gets an updated list of all subscribed habits via a DB query."""
        self.habit_subs = self.get_subscribed_habits(HabitQueryCondition.ALL)

    def get_all_non_subbed_public_habits(self) -> list[HabitData]:
        """Returns a list of all public habits that the user is not subscribed to."""
        #! doesn't scale well, limit queries to 20~100 a piece?
        habits = request.get_all_public_habits()
        subscribed_ids = {sub.data_id for sub in self.habit_subs}
        # Return only those habits the user is not subscribed to
        result = [habit for habit in habits if habit.id not in subscribed_ids]
        return result

    def _on_login(self) -> None:
        """Called on login. Checks and updates completions, streaks, etc."""
        # check if streaks broken
        for sub in self.habit_subs:
            sub.check_streak_broken()