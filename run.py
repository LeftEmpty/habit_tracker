from gui.gui import GUI
import db.controller as dbc
import db.populate_debug_data as pdd
# import atexit
import argparse

def main(debug:bool) -> None:

    dbc.db_init()
    if debug:
        pdd.populate_all()

    # atexit.register(cleanup)

    gui = GUI()
    gui.__start__() # starts GUI mainloop

if __name__ == "__main__":
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
