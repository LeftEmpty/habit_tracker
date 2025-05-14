from obj.src.habit import HabitData
from obj.src.subscription import HabitSubscription
from gui.util.gui_enums import HabitQuerryCondition
import obj.util.request_handler as request

from datetime import date


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
            self.habit_subs = self.get_subscribed_habits(HabitQuerryCondition.ALL)

        self.init_complete = True

    def __bool__(self):
        return self.user_id is not None and self.user_id >= 0

    def get_subscribed_habits(self, cond:HabitQuerryCondition=HabitQuerryCondition.ALL) -> list[HabitSubscription]:
        """_summary_

        Args:
            cond (HabitQuerryCondition): _description_

        Returns:
            list[HabitSubscription]: _description_
        """
        if cond == HabitQuerryCondition.NONE:
            return []

        subs:list[HabitSubscription] = request.get_subs_for_user(self.user_id)

        if cond == HabitQuerryCondition.ALL:
            return subs
        if cond == HabitQuerryCondition.DUE:
            for s in subs:
                if s.get_completed_state():
                    subs.remove(s)
        if cond == HabitQuerryCondition.COMPLETED:
            for s in subs:
                if not s.get_completed_state():
                    subs.remove(s)
        return subs

    def update_subscribed_habits(self) -> None:
        self.habit_subs = self.get_subscribed_habits(HabitQuerryCondition.ALL)