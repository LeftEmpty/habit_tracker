import tkinter as tk
from tkinter import ttk
from frontend.src.panels.panel import PanelBase

class Dashboard(PanelBase):
    def __init__(self, root_reference:ttk.Notebook) -> None:
        super().__init__(root_reference)
        self.setup_panel()

    def setup_panel(self) -> None:
        label = tk.Label(self, text="Dashboard", font=("Roboto", 24), bg='#000000', fg='#FFFFFF')
        label.pack(padx=24, pady=24)
    
    # @TODO query data of given day for logged in user
    
    # @TODO allow user to tick them by displaying relevant options