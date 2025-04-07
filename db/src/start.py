from sqlite_rx.server import SQLiteServer # type: ignore
from sqlite_rx.client import SQLiteClient # type: ignore
from table_definitions.completions import completions
from table_definitions.habit import habit
from table_definitions.habit_list import habit_list
from table_definitions.user import user


def start():

    # database is a path-like object giving the pathname 
    # of the database file to be opened. 
    
    # You can use ":memory:" to open a database connection to a database 
    # that resides in RAM instead of on disk

    server = SQLiteServer(database="db.sqlite",
                          bind_address="tcp://127.0.0.1:5000")
    server.start() # type: ignore

    client = SQLiteClient(connect_address="tcp://127.0.0.1:5000")
    with client:
        client.execute(user) # type: ignore
        client.execute(habit) # type: ignore
        client.execute(habit_list) # type: ignore
        client.execute(completions) # type: ignore
    server.join() # type: ignore



if __name__ == '__main__':
    start()
