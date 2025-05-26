import tkinter as tk
from tkinter import ttk
from gui.screen import ScreenBase
from gui.util.gui_enums import HabitListMode
from gui.widgets import HabitSubListWidget

# forward declaring for better type checking / overview
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui import GUI
    from obj.habit import HabitData
    from obj.subscription import Periodicity

class PublicHabitsScreen(ScreenBase):
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
        self.update_screen_title("PUBLIC HABITS")

        ttk.Label(self, text="Select a periodicity and click on the [+] button.")\
            .grid(row=1, column=0, padx=8, pady=6, sticky="w")

    def _init_habit_list(self) -> None:
        """Initializes the habit list, should be called on open_screen_event, we need a valid user.
        (User object is not yet constructed when this screen is setup during gui initialization.)"""
        if self.owning_gui.cur_user is None:
            return

        self.habit_label = ttk.Label(self, text="All public Habits")
        self.habit_label.grid(row=2, column=0, columnspan=2, pady=8, padx=8, sticky="w")

        self.habit_list = HabitSubListWidget(self, self.owning_gui, HabitListMode.DATA, subs=None, habits=self._get_public_habits_list())
        self.habit_list.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.habit_list.columnconfigure(0, weight=1)
        self.habit_list.rowconfigure(0, weight=1)

    def on_open_screen_event(self) -> None:
        """Essentially the on login function, as this one of the first things that fires once the user logs in.
        Sets up habit list & updates sidebar after log in."""
        self._init_habit_list()

    def _get_public_habits_list(self) -> list["HabitData"]:
        """Returns a list of all public habits (HabitData).
        List may be empty!"""
        # get all public habits via current user
        if self.owning_gui.cur_user:
            habits = self.owning_gui.cur_user.get_all_non_subbed_public_habits()
            return habits
        return []