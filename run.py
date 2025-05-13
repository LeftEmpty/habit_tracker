from gui.src.gui import GUI
import db.src.controller as dbc
# import atexit
from datetime import date

def main() -> None:

    dbc.db_init()
    # dbc.db_populate()

    print(date.today)

    # atexit.register(cleanup)

    gui = GUI()
    gui.__start__() # starts mainloop

if __name__ == "__main__":
    main()

def cleanup() -> None:
    pass
