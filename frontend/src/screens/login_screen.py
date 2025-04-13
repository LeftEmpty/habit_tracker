import tkinter as tk
import hashlib
from util.src.helper import validate_input
from frontend.src.screens.screen import ScreenBase


class LoginScreen(ScreenBase):
    def __init__(self, root_reference:tk.Tk) -> None:
        super().__init__(root_reference) # type: ignore

    #* **************************************** overwriting base class functionality ****************************************
    def setup_screen(self) -> None:
        # (G)root
        self.config(bg="#000")

        # Widgets
        self.login_label = tk.Label(self, text="Login", bg='#000000', fg="#FFFFFF", font=("Roboto", 32))
        self.username_label = tk.Label(self, text="Username", bg='#000000', fg="#FFFFFF", font=("Roboto", 16))
        self.username_entry = tk.Entry(self)
        self.password_label = tk.Label(self, text="Password", bg='#000000', fg="#FFFFFF", font=("Roboto", 16))
        self.password_entry = tk.Entry(self, show="*")
        self.login_button = tk.Button(self, text="Login", command=self.try_login)

        # Layout
        self.login_label.grid(row=0, column=0, columnspan=2)
        self.username_label.grid(row=1, column=0)
        self.username_entry.grid(row=2, column=0, columnspan=2)
        self.password_label.grid(row=3, column=0)
        self.password_entry.grid(row=4, column=0, columnspan=2)
        self.login_button.grid(row=5, column=0, columnspan=2)

    #* **************************************** login screen specific functionality ****************************************
    def try_login(self)->bool:
        """"""
        try_usr:str = self.username_entry.get() #type: ignore
        try_pw:str = self.password_entry.get() #type: ignore

        print(f"trying login with usr: {try_usr}, pw: {try_pw}")

        # check input
        if not try_usr or not try_pw:
            print("Username or password is empty.")
            return False

        if not validate_input(try_usr) or not validate_input(try_pw):
            print("Invalid Username or password.")
            return False

        # hash input
        hashed_usr = hashlib.sha256(try_usr.encode()).hexdigest()
        hashed_pw = hashlib.sha256(try_pw.encode()).hexdigest()

        # query db via action handler
        # @TODO call action handler login function

        return True