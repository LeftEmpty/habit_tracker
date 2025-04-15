import tkinter as tk
from tkinter import ttk
from typing import Dict
from frontend.src.screens.screen import ScreenBase
from frontend.src.panels.panel import PanelBase
from frontend.src.panels.habits_panel import HabitsPanel


class MainScreen(ScreenBase):
    def __init__(self, root_gui) -> None:
        """@TODO docstring for class"""
        super().__init__(root_gui)

    def setup_screen(self) -> None:
        # debug / info
        print("main screen setup")

        # @TODO
        self.cur_user = "Tester"
        hello_msg:str = "Hello, " + self.cur_user + "."

        # Widgets
        self.title_label = tk.Label(self, text=hello_msg, bg='#000', fg="#fff", font=("Roboto", 24), anchor="w")
        self.notebook = ttk.Notebook(self)

        # Layout
        self.title_label.pack()
        self.notebook.pack()

        # Panel instances
        self.panels: Dict[str, PanelBase] = {
            "Habits" : HabitsPanel(self.root_gui, self.notebook),
            "Habits2" : HabitsPanel(self.root_gui, self.notebook)
        }