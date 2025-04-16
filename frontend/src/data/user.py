from frontend.src.data.habits import HabitSubscription, HabitData


class User:
    def __init__(self, user_id:int, display_name:str, username:str, password:str, email:str, habits:list[HabitSubscription] = []):
        """_summary_

        Args:
            user_id (int): _description_
            display_name (str): _description_
            username (str): _description_
            password (str): _description_
            email (str): _description_
            habits (list[HabitSubscription], optional): _description_. Defaults to [].
        """
        # @TODO update / sync user data with database
            # @TODO this should also sync streaks, completions, etc.
        self.user_id:int = user_id
        self.display_name:str = display_name
        self.email:str = email
        self.username = username
        self.password = password
        self.habit_subscriptions = habits

        self.init_complete = True

    def __bool__(self):
        return self.user_id is not None

    # def __new__(cls, val=None, next=None):
    #     if val is None and next is None:
    #         return None

    def get_all_subscribed_habits(self) -> list[HabitSubscription]:
        # @TODO
        return []