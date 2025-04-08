import tkinter as tk
from tkinter import ttk
from frontend.src.screens.screen import ScreenBase

class MainScreen(ScreenBase):
    def __init__(self, root_reference) -> None:
        super().__init__(root_reference)

    def setup_screen(self) -> None:
        
        print("opened main_screen")
        login_label = tk.Label(self, text="Dashboard", bg='#000000', fg="#FFFFFF", font=("Roboto", 32))
        login_label.grid(row=0, column=0, columnspan=2)
                
        # Notebook tab view
        #notebook = ttk.Notebook(self.root)

        # Panel instances
        #self.p_login: PanelBase = LoginPanel(notebook)
        #self.p_dashboard: PanelBase = Dashboard(notebook)

        # Add to notebook
        #notebook.add(self.p_login, text="Login")
        #notebook.add(self.p_dashboard, text="Dashboard")
        #notebook.pack(expand=True, fill="both")
        