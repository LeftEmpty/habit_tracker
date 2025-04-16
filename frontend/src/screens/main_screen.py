import tkinter as tk
from tkinter import ttk
from typing import Dict
from frontend.src.screens.screen import ScreenBase
from frontend.src.panels.panel import PanelBase
from frontend.src.panels.habits_panel import HabitsPanel
from frontend.src.data.user import User

class MainScreen(ScreenBase):
    def __init__(self, root_gui, user:User) -> None:
        """@TODO docstring for class"""
        self.user = user
        super().__init__(root_gui)

    def setup_screen(self) -> None:
        if self.user == None: return

        self.hello_msg:str = "Hello " + self.user.display_name + "."

        # Widgets
        self.title_label = tk.Label(self, text=self.hello_msg, bg='#000', fg="#fff", font=("Roboto", 18, "italic"), anchor="w", pady=24)
        self.notebook = ttk.Notebook(self)

        # Layout
        self.title_label.pack()
        self.notebook.pack()

        # panel instances
        self.panels: Dict[str, PanelBase] = {
            "Habits" : HabitsPanel(self.root_gui, self.notebook),
            "Habits2" : HabitsPanel(self.root_gui, self.notebook)
        }

        # debug / info
        print("main screen setup")