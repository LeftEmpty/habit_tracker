import tkinter as tk
from frontend.src.gui import GUI
from util.src.action_handler import ActionHandler


def main() -> None:

    # Start the SQLite server in a separate process with logging
    

    action_handler = ActionHandler()
    gui = GUI(action_handler)
    gui.__start__() # starts mainloop



if __name__ == "__main__":
    main()

