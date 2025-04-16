import tkinter as tk
from frontend.src.screens.screen import ScreenBase
from util.src.validators import validate_input_login, validate_input_register
from util.src.gui_enums import PanelState, InputResponse

class LoginScreen(ScreenBase):
    #* **************************************** overwriting base class functionality ****************************************
    def __init__(self, root_gui) -> None:
        """@TODO docstring for class"""
        self.cur_panel = None
        super().__init__(root_gui)

    def setup_screen(self) -> None:
        super().setup_screen()

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
        self.failmsg_label = tk.Label(self, text="", bg='#000', fg="red", font=("Roboto", 9, "italic"), anchor="center")

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
        self.register_button.grid(row=5, column=2, pady=18)
        self.failmsg_label.grid(row=6, column=0, columnspan=3, pady=8)

        # Updatee Layout to reflect current panel state (init LOGIN)
        self.update_screen(PanelState.LOGIN)

        # debug / info
        print("login screen setup completed")


    #* **************************************** login / register functionality ****************************************
    def try_login(self) -> None:
        """Swap panel OR Check input, then pass validated and hashed input to action handler
        On faiklure: give failure response feebback"""
        if self.update_screen(PanelState.LOGIN): return

        # get input
        try_usr:str = str(self.username_entry.get())
        try_pw:str = str(self.password_entry.get())

        # validate input
        response = validate_input_login(try_usr, try_pw)
        if response != InputResponse.SUCCESS:
            self.give_failure_feedback(response)
            return

        # query db via action handler #? should i hash input here instead of action handler?
        print(f"trying login with valid input, usr: {try_usr}, pw: {try_pw}")
        if not self.root_gui.action_handler_ref.try_login_user(try_usr, try_pw):
            # @TODO handle input valid but no user found / accessible
            return


    def try_register(self) -> None:
        """Swap panel OR Check input, then pass validated and hashed input to action handler
        On faiklure: give failure response feebback."""
        if self.update_screen(PanelState.REGISTER): return

        # get input
        try_email:str = str(self.email_entry.get())
        try_usr:str = str(self.username_entry.get())
        try_pw:str = str(self.password_entry.get())
        try_pw2:str = str(self.password2_entry.get())

        # validate input
        response = validate_input_register(try_email, try_usr, try_pw, try_pw2)
        if response != InputResponse.SUCCESS:
            self.give_failure_feedback(response)
            return

        # everything is checked, create new user and send email (email service is out of scope)
        print(f"trying register with valid input, email: {try_email}, usr: {try_usr}, pw: {try_pw}, pw2: {try_pw2}")
        if not self.root_gui.action_handler_ref.try_register_user(try_email, try_usr, try_pw2, try_pw2):
            # @TODOs call action handle create register function
            return

    #* **************************************** GUI / feedback functionality ****************************************
    def update_screen(self, to_panel:PanelState) -> bool:
        """updates panel on LoginScreen, but only if necessary
        @param to_panel: new panel that screen should update to"""
        if self.cur_panel == to_panel: return False
        self.cur_panel = to_panel

        # adjust layout
        self.title_label.config(text=to_panel.value)
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

        # remove fail feedback when changing screens
        self.failmsg_label.config(text="")

        return True

    def give_failure_feedback(self, fail_reason:InputResponse) -> None:
        """sets the text of 'failmsg_lbael' element according to the received response
        @param fail_reason: response enum, value of Enum will determine text"""
        self.failmsg_label.config(text=fail_reason.value)
        print(f"fail response: {fail_reason.value}")
        # @TODO could add some fancy stuff here, e.g. 'switch statement' that marks relevant widgets red, etc.
