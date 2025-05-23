import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict
from enum import Enum
from typing import Callable

from gui.util.gui_enums import InputResponse, GUITheme
from gui.util.gui_themes import ThemeManager

from gui.src.screen import ScreenBase
from gui.src.front_screen import FrontScreen
from gui.src.home_screen import HomeScreen
from gui.src.stats_screen import StatsScreen
from gui.src.pub_habits_screen import PublicHabitsScreen

from obj.src.user import User


class GUI:
    def __init__(self)->None:
        """Basic GUI class, main root window, has instance of all panels,
        manages screens & panels and serves as root for them
        only calls util/functionality classes but does not touch data itself
        """
        self.root = tk.Tk()

        self.root.title("HabitTracker")
        self.root.geometry("1280x720")
        self.root.config()

        self.theme = ThemeManager(self.root, GUITheme.DARK)

        self.create_base_layout()

        # Initialize and store screen references in Dictionary
        self.screens: Dict[str, ScreenBase] = {
            "front" : FrontScreen(self.content_area, self),
            "home" : HomeScreen(self.content_area, self),
            "stats" : StatsScreen(self.content_area, self),
            "publics" : PublicHabitsScreen(self.content_area, self)
        }
        self.cur_screen:ttk.Frame|None = None

        # Start the GUI application
        self.cur_user:User|None = None
        self.on_startup()

    def __start__(self) -> None:
        """Starts GUI mainloop"""
        self.root.mainloop()

    def switch_theme(self, theme:GUITheme):
        """Switches theme via ThemeManager"""
        self.theme.set_theme(GUITheme.DARK)

    def create_base_layout(self) -> None:
        """Sets up the static main layout: sidebar and dynamic content area."""
        # Root container frame
        self.container = ttk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        # Notification Bar (top)
        self.notification_bar = ttk.Frame(self.container, style="NotificationDefault.TFrame", height=30)
        #self.notification_bar.pack(fill="x", side="bottom")
        self.notification_label = ttk.Label(self.notification_bar, text="", style="NotificationDefault.TLabel")
        self.notification_label.pack(side="left", padx=10)
        self.close_notification_button = ttk.Button(self.notification_bar, text="x", style="Red.TButton", command=self.close_notification_bar)
        self.close_notification_button.pack(side="right", padx=8)

        # Main Area (grid with 2 columns)
        self.main_area = ttk.Frame(self.container)
        self.main_area.pack(fill="both", expand=True)

        self.main_area.columnconfigure(0, weight=2)  # Sidebar 20%
        self.main_area.columnconfigure(1, weight=8)  # Content 80%
        self.main_area.rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ttk.Frame(self.main_area, style="Sidebar.TFrame")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.columnconfigure(0, weight=1)

        self.sidebar_logo = ttk.Label(self.sidebar, padding=12, text=" HABIT\nTRACKER", anchor="center",
                                      font=("TkDefaultFont", 26, "bold"), style="Sidebar.TLabel")
        self.sidebar_logo.grid(row=0, column=0, sticky="nsew")

        self.sidebar_btns = ttk.Frame(self.sidebar, style="Sidebar.TFrame")
        self.sidebar_btns.grid(row=1, column=0, sticky="nsew")
        self.sidebar_btns.columnconfigure(0, weight=1)

        # Content Area
        self.content_area = ttk.Frame(self.main_area, style="ContentArea.TFrame")
        self.content_area.grid(row=0, column=1, sticky="nsew")

        # Allow screens to expand inside content_area
        self.content_area.columnconfigure(0, weight=1)
        self.content_area.rowconfigure(0, weight=1)

    def on_startup(self)->bool:
        """Initializes the GUI screen system
        check if we're logged in, open appropriate screen
        (currently we don't have session tokens so we always show the front screen)

        Returns:
            bool: returns true on successful startup
        """
        #self.populate_sidebar("Home", 0, self.open_screen_home)
        self.populate_sidebar("Exit", 9, self.exit_app)

        self.open_screen("front")
        return True

    def populate_sidebar(self, btn_txt:str, btn_row:int, callback_cmd:Callable[[], None]) -> None:
        """Adds a button onto the sidebar

        Args:
            btn_txt (str): Text displayed on the ttk.Button
            btn_row (int): Row in which the ttk.Button should be placed
            callback_cmd (Callable[[], None]): The button function that takes no arguments and returns None
        """
        btn = ttk.Button(self.sidebar_btns, text=btn_txt, command=callback_cmd)
        btn.grid(row=btn_row + 1, column=0, sticky="nsew")

    def reset_sidebar(self) -> None:
        for widget in self.sidebar_btns.winfo_children():
            print ("sidebar widget being destoryed due to reset: " + widget.winfo_name())
            widget.destroy()
        self.populate_sidebar("Exit", 9, self.exit_app)

    def logout(self) -> None:
        self.cur_user = None
        self.open_screen("front")
        self.reset_sidebar()

    def exit_app(self) -> None:
        print("exit")
        if messagebox.askokcancel("Quit", "Are you sure you want to exit?"):
            self.root.destroy()
        pass

    def open_screen_home(self) -> None:
        self.open_screen("home")
    def open_screen_stats(self) -> None:
        self.open_screen("stats")
    def open_screen_publics(self) -> None:
        self.open_screen("publics")

    def open_screen(self, screen_name: str) -> None:
        """Destroys current screen frame and opens a new one inside content_area."""
        # validated get screen
        if screen_name not in self.screens:
            print("Warning: Couldn't find screen name.")
            return
        screen:ScreenBase|None = self.screens.get(screen_name)
        if screen is None or screen == self.cur_screen:
            return

        if self.cur_screen is not None:
            self.cur_screen.grid_forget()

        screen = self.screens[screen_name]
        self.cur_screen = screen

        self.cur_screen.grid(row=0, column=0)
        self.cur_screen.on_open_screen_event()

    def give_input_feedback(self, response:InputResponse) -> None:
        """Sets the text of 'inputfeedback_label' element according to the received response.
        That text/label is initially empty (and thus hidden)

        Args:
            response (InputResponse): response enum, value of Enum will determine displayedtext
        """
        self.notification_bar.pack(fill="x")
        self.notification_label.config(text=response.value)
        if response == InputResponse.SUCCESS:
            self.notification_bar.configure(style="NotificationSuccess.TFrame")
            self.notification_label.configure(style="NotificationSuccess.TLabel")
        else:
            self.notification_bar.configure(style="NotificationError.TFrame")
            self.notification_label.configure(style="NotificationError.TLabel")
            # @TODO could add some fancy stuff here, e.g. 'switch statement' that marks relevant widgets red, etc.
        print(f"input response: {response.value}")

        # Automatically hide the notification after 5 seconds
        self.notification_bar.after(5000, self.notification_bar.pack_forget)
        # @TODO bug: currently incosistent behavior e.g. spam clicking, track after() callback and rm it first

    def close_notification_bar(self) -> None:
        """Removes the notification bar"""
        self.notification_label.config(text="")
        self.notification_bar.pack_forget()