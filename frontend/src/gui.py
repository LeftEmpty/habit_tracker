import tkinter as tk
from tkinter import ttk

from frontend.src.panels.panel import PanelBase
from frontend.src.screens.screen import ScreenBase
from frontend.src.frame import FrameBase

#from frontend.src.panels.dashboard import Dashboard
#from frontend.src.screens.login_screen import LoginPanel


class GUI:
    """ Basic GUI class, main root window, has instance of all panels,
    gives panels a reference to the main root window to let them add their widgets
    only calls util/functionality classes but does not do anything else itself
    """
    def __init__(self)->None:
        print("[GUI] __init__ called")
        self.root = tk.Tk()
        self.root.title("HabitTracker")
        self.root.geometry("720x480")
        self.root.config(bg='#000', padx=12, pady=12)
                
        self.on_startup()
        
        # Launch the app
        self.root.mainloop()

    

    def on_startup(self)->bool:
        """ Initializes the GUI panel system

        @return bool: returns true on successful startup
        """
        if (not self.check_user_logged_in()):
            # show login screen
            pass
        else:
            # show main screen
            pass
        self.open_panel(self.p_dashboard)
        return True

    def open_screen(screen:FrameBase)->None:
        """
        """
        # collapse all frames
        
        # open new one
        


    def open_panel(panel:PanelBase)->None:
        """Panels are somewhat connected in that they are contained in the same notebook on the main screen"""
        panel.display_panel()
        

    def check_user_logged_in()->bool:
        # @TODO out of scope but should be added in full release
        return False

    # create and place UI elements
    def create_basic_layout(self):
        # main label
        self.label = tk.Label(self.root, text="Test Btn", font=("Roboto", 14))
        self.label.pack(pady=20)

        # button 2 - take screenshots
        self.button_screenshot = tk.Button(self.root, text="Take screenshot", command=self.capture_screenshot)
        self.button_screenshot.pack(pady=5)
