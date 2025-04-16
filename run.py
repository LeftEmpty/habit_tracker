import tkinter as tk
from frontend.src.gui import GUI
import db.src.controller as dbc
from util.src.action_handler import ActionHandler
import atexit

def main() -> None:

    # Start the SQLite server in a separate process with logging

    dbc.db_init_db()

    #atexit.register(cleanup)

    action_handler = ActionHandler()
    gui = GUI(action_handler)
    gui.__start__() # starts mainloop

if __name__ == "__main__":
    main()

def cleanup() -> None:
    pass

