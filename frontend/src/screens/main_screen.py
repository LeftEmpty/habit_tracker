import tkinter as tk
from tkinter import ttk
from frontend.src.screens.screen import ScreenBase

class LoginPanel(ScreenBase):
    def __init__(self) -> None:
        super().__init__()
        self.setup_panel()

    def setup_panel(self) -> None:
        # Notebook tab view
        notebook = ttk.Notebook(self.root)

        # Panel instances
        #self.p_login: PanelBase = LoginPanel(notebook)
        #self.p_dashboard: PanelBase = Dashboard(notebook)

        # Add to notebook
        notebook.add(self.p_login, text="Login")
        notebook.add(self.p_dashboard, text="Dashboard")
        notebook.pack(expand=True, fill="both")
        