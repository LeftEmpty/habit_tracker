# import getpass
#from cli.src.sql_controller import db_create_user, db_login_user
from sqlite_rx.client import SQLiteClient # type: ignore
from db.src.database import Database
from util.src.data_classes import Habit
from util.src.data_classes import User
from typing import Optional,Any # we use this cause pylance doesn't know sqlite classes
import hashlib

class ActionHandler:
    """ActionHandler Object that handles GUI logic, a reference is given to the GUI object.
    Calls functions (FP) on the db controller and returns values to GUI"""
    def __init__(self, db:Database):
        self.db = db
        pass

    def try_create_user(self, e_mail:str, usr:str, pw:str) -> bool:
        """gets hashed user data and creates user with it if it doesn't already exist"""

        # user_id:int | None = self.db.db_create_user(e_mail, usr, pw)

        # user_id: int | None = db_create_user(
        #     sql_client=sql_client,
        #     #display_name=display_name,
        #     username=usr,
        #     password=pw
        # )
        # return user_id
        return False

    def try_login_user(self, usr:str, pw:str, sql_client: Any) -> Optional[User]:
        """checks, formats and sends hashed data to db controller
        creates user object on success, otherwise returns false

        @return int|None: returns user_id or none, depending on success of query
        """
        pass
        # fetch data
        # user_id = db_login_user(
        #     sql_client=sql_client,
        #     username=usr,
        #     password=pw
        # )

        # check if valid, create user data object

        # successfull login - create user and give feedback to frontend
        # if user_id:
        #     # @TODO init a user object with data and store it in memory
        #     return True
        # # failed login
        # else: return False

    def try_get_all_habits(self, user_id:int) -> Optional[list[Habit]]:
        pass