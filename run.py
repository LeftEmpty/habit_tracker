import tkinter as tk
from frontend.src.gui import GUI
from util.src.action_handler import ActionHandler
#from cli.src.start import start as start_cli

import subprocess
import atexit

def main() -> None:

    # Start the SQLite server in a separate process with logging
    
    

    atexit.register(
        lambda: subprocess.call(["pkill", "-f", "db/src/start.py"])
    )
    atexit.register(cleanup)

    # start_cli()

    gui = GUI(action_handler)
    gui.__start__() # starts mainloop



if __name__ == "__main__":
    main()


