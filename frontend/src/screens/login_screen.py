import tkinter as tk
from tkinter import ttk
import hashlib
from enum import Enum
from util.src.helper import validate_input
from frontend.src.screens.screen import ScreenBase


class PanelState(Enum):
    LOGIN = "Login"
    REGISTER = "Register"


class LoginScreen(ScreenBase):
    def __init__(self, root_reference:tk.Tk) -> None:
        self.cur_panel = PanelState.LOGIN
        super().__init__(root_reference) # type: ignore


    #* **************************************** overwriting base class functionality ****************************************
    def setup_screen(self) -> None:
        """setup_screen is called on init (ScreenBase)
        Create widgets and init layout, then call """
        # (G)root
        self.config(bg="#000")

        # Widgets
        self.title_label = tk.Label(self, text="LOGIN", bg='#000', fg="#fff", font=("Roboto", 34), anchor="w")
        self.email_label = tk.Label(self, text="Email", bg='#000', fg="#fff", font=("Roboto", 13), anchor="w")
        self.email_entry = tk.Entry(self)
        self.username_label = tk.Label(self, text="Username", bg='#000', fg="#fff", font=("Roboto", 13), anchor="w")
        self.username_entry = tk.Entry(self)
        self.password_label = tk.Label(self, text="Password", bg='#000', fg="#fff", font=("Roboto", 13), anchor="w")
        self.password_entry = tk.Entry(self, show="*")
        self.password2_label = tk.Label(self, text="Confirm Password", bg='#000', fg="#fff", font=("Roboto", 13), anchor="w")
        self.password2_entry = tk.Entry(self, show="*")
        self.login_button = tk.Button(self, text="Login", fg='#fff', bg='#000', borderwidth=2, relief="flat", command=self.try_login)
        self.register_button = tk.Button(self, text="Register", fg='#fff', bg='#000', borderwidth=2, relief="flat", command=self.try_register)

        # Set Layout
        self.title_label.grid(row=0, column=0, columnspan=2, pady=8, padx=8, sticky="w")
        self.email_label.grid(row=1, column=0, padx=8, sticky="w")
        self.email_entry.grid(row=1, column=1, columnspan=2)
        self.username_label.grid(row=2, column=0, padx=8, sticky="w")
        self.username_entry.grid(row=2, column=1, columnspan=2)
        self.password_label.grid(row=3, column=0, padx=8, sticky="w")
        self.password_entry.grid(row=3, column=1, columnspan=2)
        self.password2_label.grid(row=4, column=0, padx=8, sticky="w")
        self.password2_entry.grid(row=4, column=1, columnspan=2)
        self.login_button.grid(row=5, column=0, pady=12)
        self.register_button.grid(row=5, column=2, pady=12)

        # Updatee Layout to reflect current panel state (init LOGIN)
        self.update_screen(self.cur_panel)

        # debug / info
        print("login screen setup completed")

    #* **************************************** login screen specific functionality ****************************************
    def try_login(self) -> None:
        """"""
        # check we're on the right panel, update if necessary
        if self.cur_panel == PanelState.REGISTER:
            # update screen
            self.update_screen(PanelState.LOGIN)
            return

        # get input & convert to string (type check)
        try_usr:str = str(self.username_entry.get())
        try_pw:str = str(self.password_entry.get())

        print(f"trying login with usr: {try_usr}, pw: {try_pw}")

        # validate input
        # (catch funny people)
        funny_checks:list = ["DROP_TABLE", "SELECT * FROM", "WHERE 1==1"]
        for fc in funny_checks:
            if fc in try_usr or fc in try_pw:
                print("dont do that, you know what you did =)")
                return
        if not try_usr or not try_pw:
            print("Username or password is empty.")
            return

        # hash input #? should i hash this here or in the action handler?
        hashed_usr = hashlib.sha256(try_usr.encode()).hexdigest()
        hashed_pw = hashlib.sha256(try_pw.encode()).hexdigest()

        # query db via action handler
        # @TODO call action handler login function
        #if (action_handler.login()):


    def try_register(self) -> None:
        """"""
        # check we're on the right panel, update if necessary
        if self.cur_panel == PanelState.LOGIN:
            # update screen
            self.update_screen(PanelState.REGISTER)
            return

        # get input & convert to string (type check)
        try_email:str = str(self.email_entry.get())
        try_usr:str = str(self.username_entry.get())
        try_pw:str = str(self.password_entry.get())
        try_pw2:str = str(self.password2_entry.get())

        print(f"trying register with email: {try_email}, usr: {try_usr}, pw: {try_pw}, pw2: {try_pw2}")

        #* validate input
        # check sql injection (catch funny people)
        funny_checks:list = ["DROP_TABLE", "SELECT * FROM", "WHERE 1==1"]
        for fc in funny_checks:
            if fc in try_email or fc in try_usr or fc in try_pw:
                print("dont do that, you know what you did =)")
                return
        # check email regex
        # @TODO
        # check passwords match
        if try_pw != try_pw2:
            print("Passwords do not match")
            return

        # everything is checked, create new user and send email (email service is out of scope)
        # @TODOs call action handle create register function

        return

    def update_screen(self, to_panel:Enum) -> None:
        # update title
        self.title_label.config(text=to_panel.value)

        # adjust layout
        if to_panel == PanelState.LOGIN:
            # Layout
            self.email_label.grid_remove()
            self.email_entry.grid_remove()
            self.password2_label.grid_remove()
            self.password2_entry.grid_remove()

        elif to_panel == PanelState.REGISTER:
            # Layout
            self.email_label.grid()
            self.email_entry.grid()
            self.password2_label.grid()
            self.password2_entry.grid()

        # update variable
        self.cur_panel = to_panel