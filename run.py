from gui.src.gui import GUI
import db.src.controller as dbc
import db.util.populate_debug_data as pdd
# import atexit
from datetime import date
import argparse

def main(debug:bool) -> None:

    dbc.db_init()
    if debug:
        pdd.populate_all()

    # atexit.register(cleanup)

    gui = GUI()
    gui.__start__() # starts GUI mainloop

if __name__ == "__main__":
    # TEMP
    # export PYTHONPATH=/home/pocra/Documents/projects/habit_tracker:$PYTHONPATH

    parser = argparse.ArgumentParser(description="Habit Tracker Application")
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Drops & re-creates all tables, then populates db with dummy data."
    )
    args = parser.parse_args()
    main(debug=args.debug)

def cleanup() -> None:
    pass
