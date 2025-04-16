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


def db_login_user(username: str, password: str, conn: Connection = Connection.FILE) -> int:
    """Query the db for a user login with the provided credentials.

    Args:
        username (str): username for the user
        password (str): password of the user

    Returns:
        int: user_id if successful. -1 for not found user. -2 for not unique users (if this happens i messed up tho)
    """    
    cx = sqlite3.connect(conn.value)
    result = cx.execute(
    """
    SELECT user_id FROM user WHERE username = ? AND password = ?
    """,
    (username, password)
    )

    cx.close()
    
    if result.fetchall() is None:
        log.info(f"User for {username} not found")
        return -1 # user not found
    elif len(result.fetchall()) > 1:
        log.warning(f"Multiple users found for {username}")
        return -2 # multiple users found with same credentials
    else:
        return result.fetchone()[0] # return the user_id
    

def db_create_user(display_name: str, username: str, email: str, password: str, conn: Connection = Connection.FILE) -> None:
    """Create a new user in the Database with the given credentials.
    * TODO define return type
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
    except sqlite3.Error as e:
        log.error(f"Error creating user: {e}")
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
        user_info = result.fetchall()
        return user_info
    except sqlite3.Error as e:
        log.error(f"Error retrieving user by ID of {user_id}: {e}")
        return []
    finally:
        cx.close()
    




def db_delete_user(user_id: int, conn: Connection = Connection.FILE) -> None:
    cx = sqlite3.connect(conn.value)
    result= cx.execute(
        """
        DELETE FROM user WHERE username = ?
        """,
        (user_id,)
    )



#---------------------------------------------HABIT---------------------------------------------

def db_create_habit(habit_name: str, habit_description: str, frequency: int, timeframe: str) -> None:
    result = get_db_connection().execute(
        """
        INSERT INTO habit (name, description, frequency, timeframe)
        VALUES (?, ?, ?, ?)
        """,
        (habit_name, habit_description, frequency, timeframe)
    )


#---------------------------------------------DB INIT---------------------------------------------
def db_init_db(conn: Connection = Connection.FILE) -> None:
    cx = sqlite3.connect(conn.value)
    for i in get_all_table_defs():
        cx.execute(i)
        cx.commit()

    cx.close() 

