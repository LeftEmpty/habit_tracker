from sqlite_rx.client import SQLiteClient # type: ignore
import hashlib


def create_habit(sql_client: SQLiteClient, habit_name: str, habit_description: str, frequency: int, timeframe: str) -> None: # type: ignore
    result = sql_client.execute( 
        """
        INSERT INTO habit (name, description, frequency, timeframe)
        VALUES (?, ?, ?, ?)
        """,
        habit_name, habit_description, frequency, timeframe
    )


def create_user(sql_client: SQLiteClient, display_name: str, username: str, password: str) -> None: # type: ignore
    result = sql_client.execute( 
        """
        INSERT INTO user (display_name, username, password)
        VALUES (?, ?, ?)
        """,
        display_name, hashlib.sha256(username.encode()).hexdigest(), hashlib.sha256(password.encode()).hexdigest()
    )
