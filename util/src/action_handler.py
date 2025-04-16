# import getpass
#from cli.src.sql_controller import db_create_user, db_login_user
import db.src.controller as dbc
from frontend.src.data.user import User
from typing import Optional,Any # we use this cause pylance doesn't know sqlite classes
import hashlib


class ActionHandler:
    def __init__(self):
        """ActionHandler Object that handles GUI logic, a reference is given to the GUI object.
        Calls functions (FP) on the db controller and returns values to GUI"""
        pass

    def try_register_user(self, try_usr:str, try_email:str, try_pw:str) -> bool:
        """gets hashed user data and creates user with it if it doesn't already exist"""

        hashed_usr = hashlib.sha256(try_usr.encode()).hexdigest()
        hashed_email = hashlib.sha256(try_email.encode()).hexdigest()
        hashed_pw = hashlib.sha256(try_pw.encode()).hexdigest()

        # hash input (not hashing display_name)
        if dbc.db_create_user(try_usr, hashed_usr, hashed_email, hashed_pw):
            return True
        else: return False


    def try_login_user(self, try_usr:str, try_pw:str, sql_client: Any = None)  -> bool | User:
        """checks, formats and sends hashed data to db controller
        creates user object on success, otherwise returns false

        @return int|None: returns user_id or none, depending on success of query
        """
        hashed_usr = hashlib.sha256(try_usr.encode()).hexdigest()
        hashed_pw = hashlib.sha256(try_pw.encode()).hexdigest()

        user_id:int = dbc.db_get_userid_by_credentials(hashed_usr, hashed_pw)
        if user_id == -1:
            return False

        # fetch user data, create user object and set current user on gui
        user = dbc.db_get_user_by_id(user_id)
        print(user)

        return User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4])


    def try_delete_habit(self) -> bool:
        return False


    def try_add_habit(self) -> bool:
        return False
