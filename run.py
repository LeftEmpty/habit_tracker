import tkinter as tk
from frontend.src.gui import GUI
from util.src.action_handler import ActionHandler
from db.src.database import Database
#from cli.src.start import start as start_cli

import subprocess
import atexit

def main() -> None:

    # Start the SQLite server in a separate process with logging
    with open("db_handler.log", "w") as log_file:
        # Run the script as a subprocess
        subprocess.Popen(
            ["python3", "-u", "db/src/start.py"],
            stdout=log_file,
            stderr=subprocess.STDOUT
        )

    atexit.register(
        lambda: subprocess.call(["pkill", "-f", "db/src/start.py"])
    )
    atexit.register(cleanup)

    # start_cli()

    db:Database = Database(0)
    action_handler = ActionHandler(db)
    gui = GUI(action_handler)
    gui.__start__() # starts mainloop

def cleanup():
    #server.terminate()
    #server.join()
    pass

if __name__ == "__main__":
    main()


