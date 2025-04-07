import os
from sqlite_rx.client import SQLiteClient # type: ignore
from cli.src.sql_controller import db_create_user, db_login_user
import getpass

#globals
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear') # clear console depending on os

class ActionHandler:
    """ActionHandler Object that handles GUI logic, a reference is given to the GUI object.
    Calls functions (FP) on the db controller and returns values to GUI"""
    def __init__(self, db):
        pass

    def create_user(usr:str, pw:str, sql_client: SQLiteClient) -> int | None:
        """gets hashed user data and creates user with it if it doesn't already exist"""

        user_id: int | None = db_create_user(
            sql_client=sql_client,
            #display_name=display_name,
            username=usr,
            password=pw
        )
        return user_id

    def login_user(usr:str, pw:str, sql_client: SQLiteClient) -> bool:
        """checks, formats and sends hashed data to db controller
        creates user object on success, otherwise returns false

        @return int|None: returns user_id or none, depending on success of query
        """
        user_id = db_login_user(
            sql_client=sql_client,
            username=usr,
            password=pw
        )

        # successfull login - create user and give feedback to frontend
        if user_id:
            # @TODO init a user object with data and store it in memory 
            return True
        else: return False