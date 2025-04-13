from sqlite_rx.client import SQLiteClient # type: ignore
from sqlite_rx.server import SQLiteServer # type: ignore
from sqlite_rx.client import SQLiteClient # type: ignore
from table_definitions.completions import completions
from table_definitions.habit import habit
from table_definitions.habit_list import habit_list
from table_definitions.user import user

import hashlib

class Database:
    """Database class, knows user id and db sql connection
    Contains the connection so it doesn't need to be passed around (as for example with functions in a module)
    Gets the current's user id passed and used said id to fetch data, should never fetch data not relevant to the passed id
    """

    def __init__(self, user_id:int) -> None:
        """
        @ param user_id: id of the the current user
        """
        # @TODO establish connection

        # database is a path-like object giving the pathname
        # of the database file to be opened.

        # You can use ":memory:" to open a database connection to a database
        # that resides in RAM instead of on disk

        server = SQLiteServer(database="db.sqlite",
                            bind_address="tcp://127.0.0.1:5000")
        server.start() # type: ignore

        self.client = SQLiteClient(connect_address="tcp://127.0.0.1:5000")
        with self.client:
            self.client.execute(user)
            self.client.execute(habit) # type: ignore
            self.client.execute(habit_list) # type: ignore
            self.client.execute(completions) # type: ignore

        server.join() # type: ignore
        # @TODO fetch data relevant to cur user
        pass

    def db_login_user(self,usr: str, pw: str) -> int | None:
        result = sql_client.execute(
        """
        SELECT user_id FROM user WHERE username = ? AND password = ?
        """,
        hashlib.sha256(usr.encode()).hexdigest(), hashlib.sha256(pw.encode()).hexdigest()
        )

        if (result.get("error")):
            return None
        print(result.get("items"))
        value_list: list = result.get("items") # type: ignore
        if len(value_list) == 0:
            return None
        return result.get("items")[0][0] # type: ignore

    def db_create_habit(self,habit_name: str, habit_description: str, frequency: int, timeframe: str) -> None: # type: ignore
        result = sql_client.execute(  # type: ignore
            """
            INSERT INTO habit (name, description, frequency, timeframe)
            VALUES (?, ?, ?, ?)
            """,
            habit_name, habit_description, frequency, timeframe
        )


    def db_create_user(self, e_mail: str, username: str, password: str) -> bool:
        """on creation the display_name will just be set to username, can be changed later on"""
        result = sql_client.execute(  # type: ignore
            """
            INSERT INTO user (e_mail, username, username, password)
            VALUES (?, ?, ?)
            """,
            display_name, hashlib.sha256(username.encode()).hexdigest(), hashlib.sha256(password.encode()).hexdigest()
        )
        print(result)
        if result.get("error") is None:
            return True
        return False


    def db_delete_user(self,username: str) -> None: # type: ignore
        result = sql_client.execute(  # type: ignore
            """
            DELETE FROM user WHERE username = ?
            """,
            username
            # @TODO delete all relevant completion & habit entries
        )


    # @TODO db_delete_habit