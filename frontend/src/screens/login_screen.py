import tkinter as tk
import hashlib
from util.src.endpoint_api import login_user
from frontend.src.screens.screen import ScreenBase


class LoginScreen(ScreenBase):
    def __init__(self, root_reference) -> None:
        super().__init__(root_reference)

    def setup_screen(self) -> None:
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
        self.usr_entry = username_entry.grid(row=2, column=0, columnspan=2)
        password_label.grid(row=3, column=0)
        self.pw_entry = password_entry.grid(row=4, column=0, columnspan=2)
        login_button.grid(row=6, column=0, columnspan=2, command=self.try_login)
        
    def try_login(self)->bool:
        try_usr = self.usr_entry.get()
        try_pw = self.pw_entry.get()
        hashlib.sha256(try_usr.encode()).hexdigest(), hashlib.sha256(try_pw.encode()).hexdigest()
        
        login_user(try_usr, try_pw)
        
        return True