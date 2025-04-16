from frontend.src.panels.panel import PanelBase
from frontend.src.data.habits import HabitSubscription, HabitData
import tkinter as tk
from tkinter import ttk


class HabitWidget(tk.Frame):
    def __init__(self, root:PanelBase, habit_sub:HabitSubscription):
        super().__init__(self)
        # Create widgets
        habit_name_label = tk.Label(self, text=habit_sub.habit_data.name, bg='#000', fg="#fff", font=("Roboto", 12), anchor="w")
        self.habit_checkbox_btn = tk.Button(self, text="Login", fg='#fff', bg='#000', borderwidth=2, relief="flat", command=habit_sub.add_completion_event)

        # Layout widgets
        habit_name_label.grid(row=0, column=0, pady=8)
        self.habit_checkbox_btn.grid(row=0, column=1, pady=8, padx=8)


class HabitsPanel(PanelBase):
    def __init__(self, root_gui, root_notebook:ttk.Notebook) -> None:
        super().__init__(root_gui, root_notebook)

    def setup_panel(self, panel_name:str = "Panel") -> None:
        super().setup_panel("Habits")

        # Widgets
        habit_subs_list:list[HabitSubscription] = self.root_gui.cur_user.get_all_subscribed_habits()
        for hs in habit_subs_list:
            widgt:HabitWidget = HabitWidget(self, hs)

