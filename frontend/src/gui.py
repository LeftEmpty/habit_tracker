import tkinter as tk
from tkinter import ttk
from typing import List

from frontend.src.panels.panel import PanelBase
from frontend.src.screens.screen import ScreenBase
from frontend.src.frame import FrameBase

from frontend.src.screens.login_screen import LoginScreen
from frontend.src.screens.main_screen import MainScreen
#from frontend.src.screens.login_screen import LoginPanel


class GUI:
    """ Basic GUI class, main root window, has instance of all panels,
    manages screens & panels and serves as root for them 
    only calls util/functionality classes but does not touch data itself
    """
    def __init__(self)->None:
        print("[GUI] __init__ called")
        self.root = tk.Tk()
        self.root.title("HabitTracker")
        self.root.geometry("720x480")
        self.root.config(bg='#000', padx=12, pady=12)
        
        # Initialize and store screens
        self.login_screen: LoginScreen = LoginScreen(self.root)  # Pass root to screen
        self.main_screen: MainScreen = MainScreen(self.root)  # Uncomment this line
        
        # List to store screen references
        self.screens: List[ScreenBase] = [self.login_screen, self.main_screen]

        # Start the GUI application
        self.on_startup()
        
        # Launch the app
        self.root.mainloop()


    def on_startup(self)->bool:
        """ Initializes the GUI panel system
        -> check if we're logged in, open appropriate screen
        
        @return bool: returns true on successful startup
        """
        if not self.check_user_logged_in():
            # Show login screen if user is not logged in
            self.open_screen(self.login_screen)
        else:
            # Show main screen if user is logged in
            self.open_screen(self.main_screen)
            
        return True

    def open_screen(self, screen:FrameBase)->None:
        """
        """
        # Collapse all frames
        for s in self.screens:
            s.pack_forget()
        # Show the selected screen
        screen.pack(expand=True, fill="both")
        
    def check_user_logged_in(self)->bool:
        # @TODO out of scope but should be added in full release
        return True