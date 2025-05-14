import sqlite3
import sys, os
from enum import Enum

sys.path.append(os.path.abspath("."))

from db.util.logger import log
from db.util.populate_debug_data import populate_all as populate_dummy_data
from db.src.table_definitions import get_all_table_defs


class Connection(Enum):
    TEST = "test.sqlite"
    FILE = "db.sqlite"


#* ********************************************* DB INIT *********************************************
def db_init(conn: Connection = Connection.FILE) -> None:
    """Initializes the database connection

    Args:
        conn (Connection, optional): Connection to be connected. Defaults to Connection.FILE.
    """
    for table in get_all_table_defs():
        try:
            cx = sqlite3.connect(conn.value)
            log.info("Creating table: " + str(table))
            cx.execute(table)
        except sqlite3.Error as e:
            log.error(f"Error creating table {table}: {e}")

def db_populate_dummy_data() -> None:
    populate_dummy_data()


#* ********************************************* USER *********************************************
def db_create_user(display_name:str, username:str, email:str, password:str, conn:Connection=Connection.FILE) -> bool:
    """Create a new user in the Database with the given credentials.

    Args:
        email (str): email of the new user
        display_name (str): Name to be displayed in the GUI elements.
        username (str): internal username for login and db (Unique).
        password (str): password of the new user

    Returns:
        bool: True if the user was created successfully, False otherwise.
    """
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            INSERT INTO user (display_name, username, email, password)
            VALUES (?, ?, ?, ?)
            """,
            (display_name, username, email, password)
        )
        return True
    except sqlite3.Error as e:
        log.error(f"Error creating user: {e}")
        return False
    finally:
        cx.commit()
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

def db_get_userid_by_credentials(username:str, password:str, conn:Connection=Connection.FILE) -> int:
    """Query the db for a user login with the provided credentials.

    Args:
        username (str): username for the user
        password (str): password of the user

    Returns:
        int: user_id if successful. -1 for not found user.
    """
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            SELECT user_id FROM user WHERE username = ? AND password = ?
            """,
            (username, password)
        )
        r = result.fetchall()
        if len(r) == 0 or not r:
            log.info(f"User for {username} not found")
            return -1
        else:
            return r[0][0]
    except sqlite3.Error as e:
        log.error(f"Error retrieving user by credentials of {username}: {e}")
        return -1
    finally:
        cx.close()


#* ********************************************* HABIT *********************************************
def db_create_habit_data(author_user_id:int, author_display_name:str, habit_name:str, habit_desc:str, b_public:bool, b_official:bool, last_modified:str="", conn:Connection=Connection.FILE) -> int:
    """Create a habit data entry.

    Returns:
        int:ID of habit data entry"""
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            INSERT INTO habit_data (name, description, author_name, author_user_id, public, official, last_modified)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (habit_name, habit_desc, author_display_name, author_user_id, b_public, b_official, last_modified)
        )
        if result.lastrowid:
            return result.lastrowid
        else:
            log.error(f"Error retrieving ID (result.lastrowid) of habit \"{habit_name}\" from user \"{author_display_name}\"")
            return -1
    except sqlite3.Error as e:
        log.error(f"Error creating habit {habit_name} {habit_desc}: {e}")
        return -1
    finally:
        cx.commit()
        cx.close()

def db_delete_habit_data(data_id:int, conn:Connection=Connection.FILE) -> bool:
    cx = sqlite3.connect(conn.value)
    log.info(f"Attempting to delete habit with ID of {data_id}")
    cu = cx.cursor()
    try:
        cu = cx.execute(
            """
            DELETE FROM habit_data WHERE habit_data_id = ?
            """,
            (data_id,)
        )
    except sqlite3.Error as e:
        log.error(f"Error deleting habit with ID of {data_id}: {e}")
        return False
    finally:
        cx.commit()
        cx.close()
        if cu.rowcount == 0:
            return False
        else:
            log.info("Habit deleted successfully")
            return True

def db_modify_habit_data(data_id:int, new_name:str, new_description:str, public:bool, last_modified:str, conn:Connection=Connection.FILE) -> bool:
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            UPDATE habit_data SET name = ?, description = ?, public = ?, last_modified = ? WHERE habit_data_id = ?
            """,
            (new_name, new_description, public, last_modified, data_id)
        )
        log.info(f"Successfully modified habit with ID {data_id}")
        return True
    except sqlite3.Error as e:
        log.error(f"Failed to modify habit with ID {data_id}: {e}")
        return False
    finally:
        cx.commit()
        cx.close()

def db_get_habit_data_by_id(data_id:int, conn:Connection = Connection.FILE) -> list:
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            SELECT * FROM habit_data WHERE habit_data_id = ?
            """,
            str(data_id)
        )
        return result.fetchall()
    except sqlite3.Error as e:
        log.error(f"Error getting habit with ID of {data_id}: {e}")
        return []
    finally:
        cx.commit()
        cx.close()

def db_get_habit_data_id_by_value(habit_name:str, habit_desc:str, habit_author:str, b_public:bool,conn: Connection = Connection.FILE) -> int:
    """
    ### DEPRECATED
    @TODO this function would require one of the values to be set to UNIQUE in the table."""
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            SELECT * FROM habit_data WHERE habit_name = ?, habit_desc = ?, habit_author = ?, b_public = ?
            """,
            (habit_name, habit_desc, habit_author, b_public)
        )
        return result.fetchone()[0]
    except sqlite3.Error as e:
        log.error(f"Error getting habit with name of {habit_name} by author: {habit_author}: {e}")
        return -1 # error code
    finally:
        cx.commit()
        cx.close()

def db_get_public_habits(conn: Connection = Connection.FILE) -> list:
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            SELECT * FROM habit_data WHERE public = TRUE
            """
        )
        return result.fetchall()
    except sqlite3.Error as e:
        log.error("Error getting habits flagged as public")
        return []
    finally:
        cx.commit()
        cx.close()

def db_get_subs_count_for_habit(habit_id:int, conn:Connection=Connection.FILE) -> int:
    """Returns the number of subscriptions for a given habit ID."""
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            SELECT COUNT(*) FROM habit_subscription WHERE habit_id = ?
            """,
            str(habit_id)
        )
        return result.fetchone()[0]
    except sqlite3.Error as e:
        log.error("Error getting habits flagged as public")
        return -1 # error code
    finally:
        cx.commit()
        cx.close()


#* ********************************************* SUBS *********************************************
def db_create_habit_sub(owner_user_id:int, habit_data_id:int, creation_date:str, latest_date:str|None,
    periodicity:str, cur_streak:int, max_streak:int, conn: Connection = Connection.FILE) -> int:
    """Create a habit data entry.

    Returns:
        int:ID of habit subscription entry"""
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            INSERT INTO habit_subscription (user_id, data_id, periodicity, cur_streak, max_streak, creation_date, latest_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (owner_user_id, habit_data_id, periodicity, cur_streak, max_streak, creation_date, latest_date)
        )
        if result.lastrowid:
            return result.lastrowid
        else:
            log.error(f"Error retrieving ID (result.lastrowid) of sub from user \"{owner_user_id}\"")
            return -1
    except sqlite3.Error as e:
        log.error(f"Error creating sub for habit with id {habit_data_id} on user with id {owner_user_id}: {e}")
        return -1
    finally:
        cx.commit()
        cx.close()

def db_delete_habit_sub(sub_id:int, conn:Connection=Connection.FILE) -> bool:
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            DELETE FROM habit_subscription WHERE habit_sub_id  = ?
            """,
            (sub_id,)
        )
        log.info(f"Subscription deleted successfully, ID: {sub_id}")
        return True
    except sqlite3.Error as e:
        log.error(f"Error deleting subscription with ID of {sub_id}: {e}")
        return False
    finally:
        cx.commit()
        cx.close()

def db_modifiy_sub(sub_id:int, periodicity:str, conn:Connection=Connection.FILE) -> bool:
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            UPDATE habit_subscription SET periodicty = ? WHERE habit_sub_id = ?
            """,
            (periodicity, sub_id)
        )
        return True
    except sqlite3.Error as e:
        log.error(f"Failed to modify habit subscription wiht ID {sub_id}")
        return False
    finally:
        cx.commit()
        cx.close()

def db_get_subs_for_user(user_id:int, conn:Connection=Connection.FILE) -> list:
    cx = sqlite3.connect(conn.value)
    try:
        result = cx.execute(
            """
            SELECT * FROM habit_subscription WHERE user_id = ?
            """,
            str(user_id)
        )
        return result.fetchall()
    except sqlite3.Error as e:
        log.error(f"Error getting subscriptions from user with ID of {user_id}: {e}")
        return []
    finally:
        cx.commit()
        cx.close()
