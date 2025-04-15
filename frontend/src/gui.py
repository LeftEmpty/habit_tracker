import tkinter as tk
from typing import Dict

from frontend.src.screens.screen import ScreenBase
from frontend.src.screens.login_screen import LoginScreen
from frontend.src.screens.main_screen import MainScreen

from util.src.action_handler import ActionHandler


class GUI:
    def __init__(self, action_handler:ActionHandler)->None:
        """Basic GUI class, main root window, has instance of all panels,
        manages screens & panels and serves as root for them
        only calls util/functionality classes but does not touch data itself
        """
        self.root = tk.Tk()

        self.root.title("HabitTracker")
        self.root.geometry("720x480")
        self.root.config(bg='#000', padx=12, pady=12)

        self.action_handler_ref = action_handler

        # Initialize and store screen references in Dictionary
        self.screens: Dict[str, ScreenBase] = {
            "login" : LoginScreen(self.root),
            "main" : MainScreen(self.root)
        }
        self.current_screen:tk.Frame|None = None

        # Start the GUI application
        self.user = None
        self.on_startup()


    def __start__(self) -> None:
        """Starts GUI mainloop"""
        self.root.mainloop()


    def on_startup(self)->bool:
        """Initializes the GUI panel system
        -> check if we're logged in, open appropriate screen
        (currently we don't have session tokens so we always show the login screen)
        @return bool: returns true on successful startup
        """
        self.title_label = tk.Label(self.root, text="HabitTracker", bg='#000', fg="#fff", font=("Roboto", 34), anchor="w")
        self.title_label.pack()

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

        # Collapse current screen & show new one
        if self.current_screen:
             self.current_screen.pack_forget()
        screen.pack(expand=True, fill="both")
        screen.place(in_=self.root, anchor="center", relx=.5, rely=.5)


    def check_user_logged_in(self)->bool:
        # @TODO out of scope but should be added in full release
        return not self.user is None