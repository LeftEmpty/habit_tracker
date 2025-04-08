import tkinter as tk
from tkinter import ttk
from frontend.src.screens.screen import ScreenBase

class LoginPanel(ScreenBase):
    def __init__(self) -> None:
        super().__init__()
        self.setup_panel()

    def setup_panel(self) -> None:
        # Widgets
        login_label = tk.Label(self, text="Login", bg='#000000', fg="#FFFFFF", font=("Roboto", 32))
        username_label = tk.Label(self, text="Username", bg='#000000', fg="#FFFFFF", font=("Roboto", 16))
        username_entry = tk.Entry(self)
        password_label = tk.Label(self, text="Password", bg='#000000', fg="#FFFFFF", font=("Roboto", 16))
        password_entry = tk.Entry(self, show="*")
        login_button = tk.Button(self, text="Login")

        # Layout
        login_label.grid(row=0, column=0, columnspan=2)
        username_label.grid(row=1, column=0)
        username_entry.grid(row=2, column=0, columnspan=2)
        password_label.grid(row=3, column=0)
        password_entry.grid(row=4, column=0, columnspan=2)
        login_button.grid(row=6, column=0, columnspan=2)
        