from sqlite_rx.client import SQLiteClient
from sqlite_rx.server import SQLiteServer

from util.src.data_classes import User#, Habit

from db.src.table_definitions.completions import completions
from db.src.table_definitions.habit_list import habit_list
from db.src.table_definitions.habit import habit
from db.src.table_definitions.user import user


class Database:
    """Database class, knows user id and db sql connection
    Contains the connection so it doesn't need to be passed around (as for example with functions in a module)
    Gets the current's user id passed and used said id to fetch data, should never fetch data not relevant to the passed id"""

    # database is a path-like object giving the pathname
    # of the database file to be opened.

    # You can use ":memory:" to open a database connection to a database
    # that resides in RAM instead of on disk

    def __init__(self, user_id:int) -> None:
        """ init self - establish connection
        @ param user_id: id of the the current user
        """

        # debug / info
        print("initializing database..")

        # @TODO establish connection

        if not self.is_valid_user_id(user_id):
            print("ERROR: invalid user_id found when initializing database")
            return
        else:
            self.user_id = user_id

        self.server: SQLiteServer = SQLiteServer(database="db.sqlite", bind_address="tcp://127.0.0.1:5000")
        # self.server.start()

        self.client: SQLiteClient = SQLiteClient(connect_address="tcp://127.0.0.1:5000")
        with self.client:
            self.client.execute(user)
            self.client.execute(habit)
            self.client.execute(habit_list)
            self.client.execute(completions)

        # self.server.join()
        # @TODO fetch data relevant to cur user

        # debug / info
        print("database finished initialization")

    #* ********************************** User querries **********************************

    def db_get_user_data(self, user_id:int) -> User | None:
        result = self.client.execute(
            """
            SELECT * FROM user WHERE user_id = ?
            """,
            user_id
        )
        # validate result
        if result.get("error"):
            return None
        items = result.get("items", [])
        if len(items) == 0:
            return None


        # @TODO convert the result into a useable user dataclass
        print(result.get("items"))
        #user = User()
        #return user
        return None


    def is_valid_user_id(self, user_id:int) -> bool:
        """returns true/false whether a user exists in the db with the given id"""
        # @TODO
        return True

    def is_valid_login(self, username: str, password: str) -> bool:
        # hashlib.sha256(password.encode()).hexdigest()
        result = self.client.execute(
            """
            SELECT user_id FROM user WHERE username = ? AND password = ?
            """,
            username, password
        )
        if result.get("error"):
            return False
        else: return True

    def db_create_user(self, e_mail: str, username: str, password: str) -> bool:
        """on creation the display_name will just be set to username, but it can be changed later
        input should already hashed as its in transit"""
        result = self.client.execute(
            """
            INSERT INTO user (e_mail, display_name, username, password)
            VALUES (?, ?, ?, ?)
            """,
            e_mail, username, username, password
        )
        # print(result)
        return result.get("error") is None


    def db_delete_user(self, user_id: int) -> bool:
        result = self.client.execute(
            """
            DELETE FROM user WHERE user_id = ?
            """,
            user_id
            # @TODO delete all data connected to user, i.e. completions & habit entries, etc.
        )
        return result.get("error") is None


    def db_modify_user(self, user_id:int, e_mail:str, display_name: str, username:str, password:str) -> bool:
        result = self.client.execute(
            # @TODO
            """
            UPDATE user
            SET e_mail = ?, display_name = ?, username = ?, password = ?
            WHERE user_id = ?
            """,
            e_mail, display_name, username, password, user_id
        )
        return result.get("error") is None

    #* ********************************** Habit querries **********************************

    def db_create_habit(self, habit_name: str, habit_description: str, frequency: int, timeframe: str) -> bool: 
        result = self.client.execute(
            """
            INSERT INTO habit (name, description, frequency, timeframe)
            VALUES (?, ?, ?, ?)
            """,
            habit_name, habit_description, frequency, timeframe
        )
        return result.get("error") is None


    # @TODO db_delete_habit