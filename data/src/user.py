from data.src.habits import HabitSubscription, HabitData

class User:
    def __init__(self, user_id:int, display_name:str, username:str, password:str, email:str, habits:list[HabitSubscription] = []):
        """contains only data relevant for the execution of the program,
        any data that should not be accessible in memory is only available via querries and not stored anywhere"""

        # @TODO update / sync user data with database
            # @TODO this should also sync streaks, completions, etc.

        self.user_id:int = user_id
        self.display_name:str = display_name
        self.habits = habits

    def get_all_subscribed_habits(self) -> list[HabitSubscription]:
        # @TODO
        return []