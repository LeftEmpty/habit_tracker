import tkinter as tk
from tkinter import ttk
from datetime import date
from gui.screen import ScreenBase
from gui.util.gui_enums import HabitQueryCondition, HabitListMode, InputResponse
from gui.widgets import PeriodicityHabitListPopup
from obj.subscription import HabitSubscription
from enum import Enum

# forward declaring for better type checking / overview
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui import GUI
    from obj.habit import HabitData


class StatsScreenState(Enum):
    """Enum used to determine if frontscreen is in login or register state"""
    DEFAULT = "Showing default stats."
    HABIT = "Showing habit specific stats."


class StatsScreen(ScreenBase):
    def __init__(self, root:ttk.Frame, gui:"GUI"):
        """The home screen is some sort of dashboard, showing the habits due today.
        Lets User complete habits. Also allows user to create or add new habits.

        Args:
            root (ttk.Frame): parent frame, should be the gui's content area.
            gui (GUI): root gui, used to place self or get currently logged in user, etc.
        """
        super().__init__(root, gui)

        self.cur_screen_state = StatsScreenState.DEFAULT
        self.subs:list[HabitSubscription]


    def setup_screen(self) -> None:
        """Inherited setup screen function.
        Builds UI of the home screen in this case."""
        super().setup_screen()

        self.cur_selected_sub:HabitSubscription

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Title
        self.update_screen_title("STATISTICS")

        self.habit_label = ttk.Label(self, text="Select one of your habits.")
        self.habit_label.grid(row=1, column=0, columnspan=2, pady=8, padx=8, sticky="w")

        self.habit_label = ttk.Label(self, text="Select the habit you wish to view details on via the dropdown menu \n"
                                                "and then press the Button below.", font=("TkDefaultFont", 10, "italic"))
        self.habit_label.grid(row=2, column=0, columnspan=2, pady=8, padx=8, sticky="w")

        self.show_stats_btn = ttk.Button(self, text="Show Habit Stats", command=self._show_stats)
        self.show_stats_btn.grid(row=4, column=0, padx=8, pady=12, sticky="we")

        self.default_btn = ttk.Button(self, text="Show Default Stats", command=self._show_default)
        self.default_btn.grid(row=4, column=1, padx=8, pady=12, sticky="we")

        self.periodicitylist_btn = ttk.Button(self, text="List Habits by Periodicity", command=self._open_periodicity_list_popup)
        self.periodicitylist_btn.grid(row=5, column=0, columnspan=2, padx=8, pady=0, sticky="we")

        # determined by current screen state
        self.stats_container = ttk.Frame(self, style="Sidebar.TFrame")
        self.default_container = ttk.Frame(self, style="Sidebar.TFrame")
        self.default_container.grid(row=6, column=0, columnspan=2, padx=8, pady=18, sticky="ew")
        self.stats_container.grid(row=6, column=0, columnspan=2, padx=8, pady=18, sticky="ew")

    def _show_default(self) -> None:
        """"""
        if not self.owning_gui.cur_user: return

        if self.cur_screen_state == StatsScreenState.HABIT and \
        self.stats_container != None and self.default_container != None:
            self.stats_container.grid_forget()
            self.default_container.grid(row=6, column=0, columnspan=2, padx=8, pady=18, sticky="ew")
            self.cur_screen_state = StatsScreenState.DEFAULT

    def _show_stats(self) -> None:
        """Opens the popup that lets user create new habits (subscription & data)"""
        if not self.owning_gui.cur_user: return

        if self.selected_sub_var == tk.StringVar() or not self.selected_sub_var.get():
            self.owning_gui.give_input_feedback(InputResponse.EMPTY_FIELDS)
            return

        for widget in self.stats_container.winfo_children():
            widget.destroy()

        if self.cur_screen_state == StatsScreenState.DEFAULT and \
        self.stats_container != None and self.default_container != None:
            self.default_container.grid_forget()
            self.stats_container.grid(row=6, column=0, columnspan=2, padx=8, pady=18, sticky="ew")
            self.cur_screen_state = StatsScreenState.HABIT

        # set selected sub
        for sub in self.subs:
            if sub.habit_data.name == self.selected_sub_var.get():
                self.cur_selected_sub = sub

        if not self.cur_selected_sub: return

        rate:tuple[int,int,float] = self.cur_selected_sub.get_completion_rate()

        ttk.Label(self.stats_container, style="Sidebar.TLabel", text=f"{self.cur_selected_sub.habit_data.name} - Habit Details", font=("TkDefaultFont", 14, "bold"))\
            .grid(row=0, column=0, padx=8, pady=12, sticky="w")

        ttk.Label(self.stats_container, style="Sidebar.TLabel", text=f"Creation date: {self.cur_selected_sub.creation_date.isoformat()}.")\
            .grid(row=1, column=0, padx=8, pady=4, sticky="w")
        ttk.Label(self.stats_container, style="Sidebar.TLabel", text=f"Periodicity: {self.cur_selected_sub.periodicity.value}.")\
            .grid(row=2, column=0, padx=8, pady=4, sticky="w")
        ttk.Label(self.stats_container, style="Sidebar.TLabel", text=f"Current Streak: {self.cur_selected_sub.cur_streak}.")\
            .grid(row=3, column=0, padx=8, pady=4, sticky="w")
        ttk.Label(self.stats_container, style="Sidebar.TLabel", text=f"Highest Streak: {self.cur_selected_sub.max_streak}.")\
            .grid(row=4, column=0, padx=8, pady=4, sticky="w")
        ttk.Label(self.stats_container, style="Sidebar.TLabel", text=f"Total Completions: {len(self.cur_selected_sub.get_sub_completions())}.")\
            .grid(row=5, column=0, padx=8, pady=4, sticky="w")
        ttk.Label(self.stats_container, style="Sidebar.TLabel", text=f"Completion Rate: [{rate[0]}] out of exepected [{rate[1]}] -> {rate[2]}%.")\
            .grid(row=6, column=0, padx=8, pady=4, sticky="w")

    def on_open_screen_event(self) -> None:
        # check user and get subs
        if self.owning_gui.cur_user is None: return
        self.subs = self._get_user_subs_list()

        # Initialize widgets that require a valid user
        self._init_habit_dropdown()
        self._init_default_stats()

        self._show_default()

    def _init_habit_dropdown(self) -> None:
        """Initializes the habit list, should be called on open_screen_event, we need a valid user.
        (User object is not yet constructed when this screen is setup during gui initialization.)"""
        self.selected_sub_var = tk.StringVar()
        self.periodicity_menu = ttk.Combobox(self, textvariable=self.selected_sub_var, state="readonly")
        self.periodicity_menu['values'] = [sub.habit_data.name for sub in self.subs]
        self.periodicity_menu.grid(row=3, column=0, columnspan=2, padx=8, pady=18, sticky="we")

    def _init_default_stats(self) -> None:
        """Initializes the default stats shown to the user."""
        if not self.owning_gui.cur_user:
            return

        for widget in self.default_container.winfo_children():
            widget.destroy()

        best_cur = (0, "No streaks yet.")
        best_max = (0, "No streaks yet.")

        oldest = (date.today(), "No habits found.")

        easiest:tuple[float, str, int] = (0.00, "No habits found.", 0) # success rate, habit data name, expected completions
        hardest:tuple[float, str, int] = (100.00, "No habits found.", 0)

        total_compl_done:int = 0
        total_compl_exp:int = 0

        for s in self.subs:
            # streaks
            if s.cur_streak > best_cur[0]:
                best_cur = (s.cur_streak, s.habit_data.name)
            if s.max_streak > best_max[0]:
                best_max = (s.max_streak, s.habit_data.name)

            # oldest
            if s.creation_date < oldest[0]:
                oldest = (s.creation_date, s.habit_data.name)

            # easiest / hardest - prioritize habits with higher number of expected completions
            rate:tuple[int, int, float] = s.get_completion_rate()
            if rate[2] > easiest[0] or (rate[2] == easiest[0] and rate[1] > easiest[2]):
                easiest = (rate[2], s.habit_data.name, rate[1])
            if rate[2] < hardest[0] or (rate[2] == hardest[0] and rate[1] > hardest[2]):
                hardest = (rate[2], s.habit_data.name, rate[1])
            total_compl_done += rate[0]
            total_compl_exp += rate[1]

        ttk.Label(self.default_container, style="Sidebar.TLabel", text=f"{self.owning_gui.cur_user.display_name}'s Stats", font=("TkDefaultFont", 14, "bold"))\
            .grid(row=0, column=0, padx=8, pady=12, sticky="w")

        if total_compl_done + total_compl_exp == 0:
            avg_compl_rate:float = 0
        else:
            avg_compl_rate:float = round((total_compl_done / total_compl_exp) * 100, 2)

        if not len(self.subs) > 0:
            ttk.Label(self.default_container, style="Sidebar.TLabel", text="No Habits found, create or add some first.")\
                .grid(row=1, column=0, padx=8, pady=4, sticky="w")
            return

        ttk.Label(self.default_container, style="Sidebar.TLabel", text=f"Best current Streak: [{best_cur[0]}] for habit [{best_cur[1]}].")\
            .grid(row=1, column=0, padx=8, pady=4, sticky="w")
        ttk.Label(self.default_container, style="Sidebar.TLabel", text=f"Best all-time Streak: [{best_max[0]}] for habit [{best_max[1]}].")\
            .grid(row=2, column=0, padx=8, pady=4, sticky="w")

        ttk.Label(self.default_container, style="Sidebar.TLabel", text=f"Oldest Habit: [{oldest[1]}] created on: [{oldest[0]}]")\
            .grid(row=3, column=0, padx=8, pady=4, sticky="w")

        ttk.Label(self.default_container, style="Sidebar.TLabel", text=f"Hardest Habit: [{hardest[1]}] success rate: [{hardest[0]}%]")\
            .grid(row=4, column=0, padx=8, pady=4, sticky="w")
        ttk.Label(self.default_container, style="Sidebar.TLabel", text=f"Easiest Habit: [{easiest[1]}] success rate: [{easiest[0]}%]")\
            .grid(row=5, column=0, padx=8, pady=4, sticky="w")

        ttk.Label(self.default_container, style="Sidebar.TLabel", text=f"Avg. Comlpetion Rate: [{avg_compl_rate}%], ({total_compl_done}/{total_compl_exp})")\
            .grid(row=6, column=0, padx=8, pady=4, sticky="w")


    def _open_periodicity_list_popup(self) -> None:
        """Opens popup that contains list of all subs listed/ordered by their periodidicty."""
        if self.owning_gui:
            PeriodicityHabitListPopup(self.owning_gui, self.subs)

    def _get_user_subs_list(self) -> list["HabitSubscription"]:
        """"""
        # get all habits
        if self.owning_gui.cur_user:
            return self.owning_gui.cur_user.get_subscribed_habits(HabitQueryCondition.ALL)
        else:
            print("Invalid user")
            return []