from datetime import date, timedelta

import obj.request_handler as request

# forward declaring for better overview
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from obj.user import User


class HabitData:
    def __init__(self, name:str, desc:str, author_id:int, b_public:bool = False, b_official:bool = False, author_name:str="", habit_id:int = -2):
        """Data class for keeping track of habit data, should reflect the respecive db entry.

        Args:
            name (str): _description_
            desc (str): _description_
            author_id (int): _description_
            b_public (bool, optional): _description_. Defaults to False.
            b_official (bool, optional): _description_. Defaults to False.
            author_name (str, optional): _description_. Defaults to "".
            habit_id (int, optional): _description_. Defaults to -2.
        """
        self.id:int = habit_id # updated once it's registered
        self.name:str = name
        self.desc:str = desc
        self.author_id:int = author_id
        self.b_public:bool = b_public
        self.b_official:bool = b_official
        # self.last_modified:date = date.today()

        if author_name != "":
            self.author_name:str = author_name
        else:
            self.author_name = request.get_user_displayname(author_id)

        if self.id == -2:
            self.register_self()

    def __bool__(self) -> bool:
        return self.id is not None and self.id >= 0

    def modify_data(self, new_name:str, new_desc:str, b_public:bool) -> None:
        """Updates data by modifying it locally and then requesting the change to be applied in DB.

        Args:
            new_name (str): new name for this object
            new_desc (str): new desc for this object
            b_public (bool): new public setting for this object
        """
        self.name = new_name
        self.desc = new_desc
        self.b_public = b_public
        self.last_modified = date.today()
        request.modify_habit_data(self)

    def is_registered(self) -> bool:
        """Returns true if habit has been registered properly, i.e. if this object reflects an entry in DB.
        This is done by checking if the data object has a valid ID

        Returns:
            bool: returns ID >= 0 (-2 is default when unset)
        """
        return self.id >= 0

    def register_self(self) -> int:
        """Saves itself (this habit data) to the database.
        May not create a new entry if data is missing or an identical entry is found.

        Returns:
            int: returns the ID of the habit data entry (even if it's already registered), ERROR CODE: -1 [incomplete data]
        """
        if not self.is_data_complete():
            print(f"Habit \"{self.name}\" cannot register, incomplete data.")
            return -1
        if self.id >=0:
            print(f"Habit \"{self.name}\" already registered in database.")
            return self.id

        # create habit_data entry in table get resulting self.id, error code -1
        new_id = request.create_new_habit_via_obj(self)
        if new_id != -1:
            self.id = new_id
            print(f"Habit \"{self.name}\" registered self to database.")
            return new_id
        else:
            print(f"Error: Habit couldnt register \"{self.name}\" self to database.")
            return -1

    def is_data_complete(self) -> bool:
        """Checks that all dada required to register has been set

        Returns:
            bool: False if any of the data is None/empty, True if all have been set
        """
        if self.name is None or self.name == "": return False
        if self.desc is None or self.desc == "": return False
        return True

    def get_subscriber_count(self) -> int:
        """Returns the number of users that are subscribed to this habit

        Raises:
            a: _description_
            ValueError: _description_

        Returns:
            int: sub-count, nr of users subscribed to this habit
        """
        # this ensures that this object is initialized completetly and 'connected' to the db, i.e. ID is valid
        if self.is_registered():
            count = request.get_habit_subs_count(self.id)
            return count
        return -1
