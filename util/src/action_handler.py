# import getpass
#from cli.src.sql_controller import db_create_user, db_login_user
from sqlite_rx.client import SQLiteClient # type: ignore
from db.src.database import get_user_by_login
from typing import Optional,Any # we use this cause pylance doesn't know sqlite classes
import hashlib


class ActionHandler:
    def __init__(self):
        """ActionHandler Object that handles GUI logic, a reference is given to the GUI object.
        Calls functions (FP) on the db controller and returns values to GUI"""
        pass

    def try_create_user(self, e_mail:str, usr:str, pw:str) -> bool:
        """gets hashed user data and creates user with it if it doesn't already exist"""

        # user_id:int | None = self.db.db_create_user(e_mail, usr, pw)

        # user_id: int | None = db_create_user(
        #     sql_client=sql_client,
        #     #display_name=display_name,
        #     username=usr,
        #     password=pw``
        # )
        # return user_id
        return False

    def try_login_user(self, try_usr:str, try_pw:str, sql_client: Any = None)  -> bool:
        """checks, formats and sends hashed data to db controller
        creates user object on success, otherwise returns false

        @return int|None: returns user_id or none, depending on success of query
        """

        # hash input
        hashed_usr = hashlib.sha256(try_usr.encode()).hexdigest()
        hashed_pw = hashlib.sha256(try_pw.encode()).hexdigest()

        # query database with user data
        user_result = get_user_by_login(hashed_usr, hashed_pw)
        print(user_result)
        return False

        # print(user_result)
        # if (user_result.get("error") or len(user_result.get("items")) == 0):
        #     return False
        # # @TODO create user with fetched data and set current user (in gui)
        # user_data = user_result.get("items")[0][0]
        # return True

    def try_delete_habit(self) -> bool:
        return False

    def try_add_habit(self) -> bool:
        return False