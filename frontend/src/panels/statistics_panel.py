import tkinter as tk
from tkinter import ttk
from frontend.src.panels.panel import PanelBase

class StatsPanel(PanelBase):
    def __init__(self, root_gui, root_notebook:ttk.Notebook) -> None:
        super().__init__(root_gui, root_notebook)

    def setup_panel(self, panel_name:str = "Panel") -> None: # override
        super().setup_panel("Statistics")

        label = tk.Label(self, text="Dashboard", font=("Roboto", 24), bg='#000000', fg='#FFFFFF')
        label.pack(padx=24, pady=24)

    # @TODO query data of given day for logged in user

    # @TODO allow user to tick them by displaying relevant options