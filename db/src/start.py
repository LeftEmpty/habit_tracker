from sqlite_rx.server import SQLiteServer


def start():

    # database is a path-like object giving the pathname 
    # of the database file to be opened. 
    
    # You can use ":memory:" to open a database connection to a database 
    # that resides in RAM instead of on disk

    server = SQLiteServer(database="db.sqlite",
                          bind_address="tcp://127.0.0.1:5000")
    server.start()
    server.join()

if __name__ == '__main__':
    start()
