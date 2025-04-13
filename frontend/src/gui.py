import tkinter as tk
from typing import Dict

from util.src.action_handler import ActionHandler

#from frontend.src.frame import FrameBase
#from frontend.src.panels.panel import PanelBase
from frontend.src.screens.screen import ScreenBase

from frontend.src.screens.login_screen import LoginScreen
from frontend.src.screens.main_screen import MainScreen
#from frontend.src.screens.login_screen import LoginPanel


class GUI:
    """ Basic GUI class, main root window, has instance of all panels,
    manages screens & panels and serves as root for them
    only calls util/functionality classes but does not touch data itself
    """
    def __init__(self, root:tk.Tk, action_handler:ActionHandler)->None:
        print("[GUI] __init__ called")
        root.title("HabitTracker")
        root.geometry("720x480")
        root.config(bg='#000', padx=12, pady=12)

        # Initialize and store screen references in Dictionary
        self.screens: Dict[str, ScreenBase] = {
            "login" : LoginScreen(root),
            "main" : MainScreen(root)
        }
        self.current_screen:tk.Frame|None = None

        # Start the GUI application
        self.user = None
        self.on_startup()

    def on_startup(self)->bool:
        """Initializes the GUI panel system
        -> check if we're logged in, open appropriate screen
        (currently we don't have session tokens so we always show the login screen)
        @return bool: returns true on successful startup
        """
        #* (note to future self: this is c-style 'if ? :' )
        self.open_screen("main") if self.check_user_logged_in() else self.open_screen("login")

        return True

    def open_screen(self, screen_to_show:str)->None:
        """Changes the screen of the whole app
        Changes inside of screens (i.e. panels) are handled by screen themselves (ScreenBase)"""

        # validated get screen
        if screen_to_show not in self.screens:
            return
        screen:ScreenBase|None = self.screens.get(screen_to_show)
        if screen is None: return

        # Collapse current screen
        if self.current_screen:
             self.current_screen.pack_forget()
        # Show the selected screen
        screen.pack(expand=True, fill="both")

    def check_user_logged_in(self)->bool:
        # @TODO out of scope but should be added in full release
        return True