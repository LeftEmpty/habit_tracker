import tkinter as tk
from tkinter import ttk
from gui.screen import ScreenBase
from gui.util.gui_enums import HabitQueryCondition, HabitListMode
from gui.widgets import HabitSubListWidget, HabitCreationPopup

# forward declaring for better type checking / overview
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui import GUI
    from obj.subscription import HabitSubscription

class HomeScreen(ScreenBase):
    def __init__(self, root:ttk.Frame, gui:"GUI"):
        """The home screen is some sort of dashboard, showing the habits due today.
        Lets User complete habits. Also allows user to create or add new habits.

        Args:
            root (ttk.Frame): parent frame, should be the gui's content area.
            gui (GUI): root gui, used to place self or get currently logged in user, etc.
        """
        super().__init__(root, gui)

    def setup_screen(self) -> None:
        """Inherited setup screen function.
        Builds UI of the home screen in this case."""
        super().setup_screen()

        # Title
        self.update_screen_title("HOME")

        # Buttons
        self.create_new_btn = ttk.Button(self, text="Create Habit", command=self._create_habit)
        self.create_new_btn.grid(row=3, column=0, padx=8, pady=18, sticky="we")

        self.add_habit_btn = ttk.Button(self, text="Add Habit", command=self.owning_gui.open_screen_publics)
        self.add_habit_btn.grid(row=3, column=1, padx=8, pady=18, sticky="we")

    def _init_habit_list(self) -> None:
        """Initializes the habit list, should be called on open_screen_event, we need a valid user.
        (User object is not yet constructed when this screen is setup during gui initialization.)"""
        if self.owning_gui.cur_user is None:
            return

        self.habit_label = ttk.Label(self, text="Today's Habits")
        self.habit_label.grid(row=1, column=0, columnspan=2, pady=8, padx=8, sticky="w")

        self.habit_list = HabitSubListWidget(self, self.owning_gui, HabitListMode.SUB, None, self._get_user_subs_list())
        self.habit_list.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.habit_list.columnconfigure(0, weight=1)
        self.habit_list.rowconfigure(0, weight=1)

    def _create_habit(self) -> None:
        """Opens the popup that lets user create new habits (subscription & data)"""
        if self.owning_gui.cur_user:
            HabitCreationPopup(self.owning_gui, self.owning_gui.cur_user, self.habit_list.reload_list)

    def on_open_screen_event(self) -> None:
        """Essentially the on login function, as this one of the first things that fires once the user logs in.
        Sets up habit list & updates sidebar after log in."""
        self._init_habit_list()
        self.owning_gui.populate_sidebar("Home", 0, self.owning_gui.open_screen_home)
        self.owning_gui.populate_sidebar("Statistics", 1, self.owning_gui.open_screen_stats)
        self.owning_gui.populate_sidebar("Public Habits", 2, self.owning_gui.open_screen_publics)
        self.owning_gui.populate_sidebar("Logout", 8, self.owning_gui.logout)

    def _get_user_subs_list(self) -> list["HabitSubscription"]:
        """"""
        # get all habits
        if self.owning_gui.cur_user:
            return self.owning_gui.cur_user.get_subscribed_habits(HabitQueryCondition.RELEVANT_TODAY)
        else:
            print("Invalid user")
            return []