import tkinter as tk
from tkinter import ttk
from gui.src.screen import ScreenBase
from gui.util.gui_enums import HabitQueryCondition, HabitListMode, InputResponse
from gui.util.widgets import HabitSubListWidget, HabitCreationPopup
from obj.src.subscription import HabitSubscription

# forward declaring for better type checking / overview
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.src.gui import GUI
    from obj.src.habit import HabitData

class StatsScreen(ScreenBase):
    def __init__(self, root:ttk.Frame, gui:"GUI"):
        """The home screen is some sort of dashboard, showing the habits due today.
        Lets User complete habits. Also allows user to create or add new habits.

        Args:
            root (ttk.Frame): parent frame, should be the gui's content area.
            gui (GUI): root gui, used to place self or get currently logged in user, etc.
        """
        super().__init__(root, gui)

        self.stats_container = ttk.Frame(self, style="Sidebar.TFrame")

    def setup_screen(self) -> None:
        """Inherited setup screen function.
        Builds UI of the home screen in this case."""
        super().setup_screen()

        self.cur_selected_sub:HabitSubscription

        # Title
        self.update_screen_title("STATISTICS")

        # Habit details
        self.habit_label = ttk.Label(self, text="Select one of your habits.")
        self.habit_label.grid(row=1, column=0, pady=8, padx=8, sticky="w")

        self.habit_label = ttk.Label(self, text="Select the habit you wish to view details on via the dropdown menu \n"
                                                "and then press the Button below.", font=("TkDefaultFont", 10, "italic"))
        self.habit_label.grid(row=2, column=0, pady=8, padx=8, sticky="w")

        self.create_new_btn = ttk.Button(self, text="Show Habit Stats", command=self._show_stats)
        self.create_new_btn.grid(row=4, column=0, padx=8, pady=18, sticky="ew")

    def _init_habit_dropdown(self) -> None:
        """Initializes the habit list, should be called on open_screen_event, we need a valid user.
        (User object is not yet constructed when this screen is setup during gui initialization.)"""
        if self.owning_gui.cur_user is None:
            return

        self.selected_sub_var = tk.StringVar()
        self.periodicity_menu = ttk.Combobox(self, textvariable=self.selected_sub_var, state="readonly")
        self.periodicity_menu['values'] = [sub.habit_data.name for sub in self._get_user_subs_list()]
        self.periodicity_menu.grid(row=3, column=0, padx=8, pady=18, sticky="ew")

    def _show_stats(self) -> None:
        """Opens the popup that lets user create new habits (subscription & data)"""
        if not self.owning_gui.cur_user: return

        if self.selected_sub_var == tk.StringVar():
            self.owning_gui.give_input_feedback(InputResponse.EMPTY_FIELDS)

        # set selected sub
        for sub in self._get_user_subs_list():
            if sub.habit_data.name == self.selected_sub_var.get():
                self.cur_selected_sub = sub

        if not self.cur_selected_sub: return

        rate:tuple[int,int,float] = self.cur_selected_sub.get_completion_rate()

        # widgets
        self.stats_container.grid(row=5, column=0, padx=8, pady=18, sticky="ew")

        ttk.Label(self.stats_container, style="Sidebar.TLabel", text=f"{self.cur_selected_sub.habit_data.name} - details", font=("TkDefaultFont", 14, "bold"))\
            .grid(row=0, column=0, padx=8, pady=12, sticky="w")

        ttk.Label(self.stats_container, style="Sidebar.TLabel", text=f"Creation date: {self.cur_selected_sub.creation_date.isoformat()}.")\
            .grid(row=1, column=0, padx=8, pady=6, sticky="w")
        ttk.Label(self.stats_container, style="Sidebar.TLabel", text=f"Periodicity: {self.cur_selected_sub.periodicity.value}.")\
            .grid(row=2, column=0, padx=8, pady=6, sticky="w")
        ttk.Label(self.stats_container, style="Sidebar.TLabel", text=f"Current Streak: {self.cur_selected_sub.cur_streak}.")\
            .grid(row=3, column=0, padx=8, pady=6, sticky="w")
        ttk.Label(self.stats_container, style="Sidebar.TLabel", text=f"Highest Streak: {self.cur_selected_sub.max_streak}.")\
            .grid(row=4, column=0, padx=8, pady=6, sticky="w")
        ttk.Label(self.stats_container, style="Sidebar.TLabel", text=f"Total Completions: {len(self.cur_selected_sub.get_sub_completions())}.")\
            .grid(row=5, column=0, padx=8, pady=6, sticky="w")
        ttk.Label(self.stats_container, style="Sidebar.TLabel", text=f"Completions Rate: [{rate[0]}] out of exepected [{rate[1]}] -> {rate[2]}%.")\
            .grid(row=6, column=0, padx=8, pady=6, sticky="w")

    def _add_habit(self) -> None:
        """Changes gui to the PublicHabitsScreen to let User browse habits"""
        self.owning_gui.open_screen("public_habits")
        pass

    def on_open_screen_event(self) -> None:
        """"""
        self.subs = self._get_user_subs_list()
        self._init_habit_dropdown()
        if self.stats_container:
            self.stats_container.grid_forget()

    def _get_user_subs_list(self) -> list["HabitSubscription"]:
        """"""
        # get all habits
        if self.owning_gui.cur_user:
            return self.owning_gui.cur_user.get_subscribed_habits(HabitQueryCondition.ALL)
        else:
            print("Invalid user")
            return []