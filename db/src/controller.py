import hashlib
import sqlite3
import sys, os
from enum import Enum

sys.path.append(os.path.abspath("."))

from db.util.logger import log
from db.src.table_definitions import get_all_table_defs

class Connection(Enum):
    TEST = "test.sqlite"
    FILE = "db.sqlite"


def db_get_userid_by_credentials(username: str, password: str, conn: Connection = Connection.FILE) -> int:
    """Query the db for a user login with the provided credentials.

    Args:
        username (str): username for the user
        password (str): password of the user

    Returns:
        int: user_id if successful. -1 for not found user.
    """
    cx = sqlite3.connect(conn.value)
    result = cx.execute(
    """
    SELECT user_id FROM user WHERE username = ? AND password = ?
    """,
    (username, password)
    )

    result = result.fetchall()
    cx.close()
    if len(result) == 0 or not result:
        log.info(f"User for {username} not found")
        return -1
    else:
        return result[0][0]


def db_create_user(display_name: str, username: str, email: str, password: str, conn: Connection = Connection.FILE) -> bool:
    """Create a new user in the Database with the given credentials.
    Args:
        display_name (str): Name to be displayed in the GUI elements
        username (str): internal username for login and db (Unique)
        password (str): password of the new user
    """

    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            INSERT INTO user (display_name, email, username, password)
            VALUES (?, ?, ?, ?)
            """,
            (display_name, email, username, password)
        )
        return True
    except sqlite3.Error as e:
        log.error(f"Error creating user: {e}")
        return False
    finally:
        cx.commit()
        cx.close()


def db_get_user_by_id(user_id: int, conn: Connection = Connection.FILE) -> list:
    """Get a user by their ID.
    Args:
        user_id (int): The ID of the user to retrieve.
    Returns:
        list: A list containing the user's information, or an empty list if no user is found.
    """
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            SELECT * FROM user WHERE user_id = ?
            """,
            (user_id,)
        )

        return result.fetchall()
    except sqlite3.Error as e:
        log.error(f"Error retrieving user by ID of {user_id}: {e}")
        return []
    finally:
        cx.close()


def db_delete_user(user_id: int, conn: Connection = Connection.FILE) -> bool:
    cx: sqlite3.Connection = sqlite3.connect(conn.value)
    log.info(f"Attempting to delete user with ID of {user_id}")
    cu: sqlite3.Cursor = cx.cursor()
    try:
        cu: sqlite3.Cursor = cu.execute(
            """
            DELETE FROM user WHERE user_id  = ?
            """,
            (user_id,)
        )
    except sqlite3.Error as e:
        log.error(f"Error deleting user with ID of {user_id}: {e}")
        return False
    finally:
        cx.commit()
        cx.close()
        if cu.rowcount == 0:
            return False
        else:
            log.info("User deleted successfully")
            return True



#---------------------------------------------HABIT---------------------------------------------

def db_create_habit(user_id: int, habit_name: str, habit_description: str = "", public: bool = False, conn: Connection = Connection.FILE) -> None:
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
        """
        INSERT INTO habit_data (name, description, public, user_id)
        VALUES (?, ?, ?, ?)
        """,
        (habit_name, habit_description, public, user_id)
    )
    except sqlite3.Error as e:
        log.error(f"Error creating habit {habit_name} {habit_description}: {e}")
    finally:
        cx.commit()
        cx.close()


def db_get_habit_by_id(habit_id: int, conn: Connection = Connection.FILE) -> list:
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
        """
        SELECT * FROM habit_data WHERE habit_id = ?
        """,
        str(habit_id)
    )
        return result.fetchall()
    except sqlite3.Error as e:
        log.error(f"Error getting habit with ID of {habit_id}: {e}")
        return []
    finally:
        cx.commit()
        cx.close()

def db_delete_habit(habit_id: int, conn: Connection = Connection.FILE) -> bool:
    cx = sqlite3.connect(conn.value)
    log.info(f"Attempting to delete habit with ID of {habit_id}")
    cu = cx.cursor()
    try:
        cu = cx.execute(
        """
        DELETE FROM habit_data WHERE habit_id = ?
        """,
        (habit_id,)
    )
    except sqlite3.Error as e:
        log.error(f"Error deleting habit with ID of {habit_id}: {e}")
        return False
    finally:
        cx.commit()
        cx.close()
        if cu.rowcount == 0:
            return False
        else:
            log.info("Habit deleted successfully")
            return True

def db_modify_habit(habit_id: int, new_name: str, new_description: str = "", public: bool = False, conn: Connection = Connection.FILE) -> bool:
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            UPDATE habit SET name = ?, description = ?, public = ? WHERE habit_id = ?
            """,
            (new_name, new_description, public, habit_id)
        )
    except sqlite3.Error as e:
        log.error(f"Error modifying habit with ID of {habit_id}: {e}")
        return False
    finally:
        cx.commit()
        cx.close()
        return True


#---------------------------------------------DB INIT---------------------------------------------
def db_init_db(conn: Connection = Connection.FILE) -> None:

    for i in get_all_table_defs():
        try:
            cx = sqlite3.connect(conn.value)
            log.info("Creating table: " + str(i))
            cx.execute(i)
        except sqlite3.Error as e:
            log.error(f"Error creating table {i}: {e}")
