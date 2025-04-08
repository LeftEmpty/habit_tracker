from sqlite_rx.client import SQLiteClient # type: ignore
import hashlib



def db_login_user(sql_client: SQLiteClient, username: str, password: str) -> int | None:
    result = sql_client.execute(
    """
    SELECT user_id FROM user WHERE username = ? AND password = ?
    """,
    hashlib.sha256(username.encode()).hexdigest(), hashlib.sha256(password.encode()).hexdigest()
    )
    
    if (result.get("error")):
        return None
    print(result.get("items"))
    value_list: list = result.get("items") # type: ignore
    if len(value_list) == 0:
        return None
    return result.get("items")[0][0] # type: ignore



def db_create_habit(sql_client: SQLiteClient, habit_name: str, habit_description: str, frequency: int, timeframe: str) -> None: # type: ignore
    result = sql_client.execute(  # type: ignore
        """
        INSERT INTO habit (name, description, frequency, timeframe)
        VALUES (?, ?, ?, ?)
        """,
        habit_name, habit_description, frequency, timeframe
    )


def db_create_user(sql_client: SQLiteClient, display_name: str, username: str, password: str) -> bool:
    result = sql_client.execute(  # type: ignore
        """
        INSERT INTO user (display_name, username, password)
        VALUES (?, ?, ?)
        """,
        display_name, hashlib.sha256(username.encode()).hexdigest(), hashlib.sha256(password.encode()).hexdigest()
    )
    print(result)
    if result.get("error") is None:
        return True
    return False
    

def db_delete_user(sql_client: SQLiteClient, username: str) -> None: # type: ignore
    result = sql_client.execute(  # type: ignore
        """
        DELETE FROM user WHERE username = ?
        """,
        username
    )