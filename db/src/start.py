from sqlite_rx.server import SQLiteServer


def start() -> None: 
    server = SQLiteServer(database="db.sqlite",
                          bind_address="tcp://127.0.0.1:5000")
    server.start()
    server.join()

start()