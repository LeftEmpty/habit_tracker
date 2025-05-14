import tkinter as tk
from tkinter import ttk

from gui.util.gui_enums import GUITheme


class ThemeManager:
    def __init__(self, root:tk.Tk, theme:GUITheme):
        """Essentially the CSS file. Sets default styles for ttk widgets. [WIP]
        Currently only one theme but the functionality can support multiple."""
        self.root = root
        self.theme:GUITheme = theme

        self.style = ttk.Style(self.root)
        self.set_theme(self.theme)

    def set_theme(self, theme:GUITheme) -> None:
        self.theme = theme
        if self.theme == GUITheme.DARK:
            self._set_dark_theme()
        elif self.theme == GUITheme.LIGHT:
            self._set_light_theme() # @TODO implement light theme
        elif self.theme == GUITheme.DEFAULT:
            self._set_dark_theme() # @TODO implement default them
        else:
            raise ValueError("Unsupported theme")

    def _set_dark_theme(self):
        self.style.theme_use('clam')

        # Common Colors
        bg_dark = "#333333"
        bg_light = "#ffffff"
        bg_success = "#2ecc71"  # (green)
        bg_error = "#e74c3c"    # (red)
        fg_text_light = "#ffffff"
        fg_text_dark = "#2c2c2c"
        accent_color = "#5D96BE"

        # Base Frame (for main areas)
        self.style.configure("ContentArea.TFrame", background=bg_dark)
        self.style.configure("Sidebar.TFrame", background=bg_light)
        self.style.configure("NotificationDefault.TFrame", background=accent_color)
        self.style.configure("NotificationSuccess.TFrame", background=bg_success)
        self.style.configure("NotificationError.TFrame", background=bg_error)

        # Labels
        self.style.configure("TLabel", background=bg_dark, foreground=fg_text_light, font=("Roboto", 12))
        self.style.configure("Sidebar.TLabel", background=bg_light, foreground=fg_text_dark, font=("Roboto", 12))
        self.style.configure("NotificationDefault.TLabel", background=accent_color, foreground=fg_text_light, font=("Roboto", 12, "bold"))
        self.style.configure("NotificationSuccess.TLabel", background=bg_success, foreground=fg_text_light, font=("Roboto", 12, "bold"))
        self.style.configure("NotificationError.TLabel", background=bg_error, foreground=fg_text_light, font=("Roboto", 12, "bold"))

        # Buttons
        self.style.configure("TButton",
            background=bg_light,  # start with sidebar color
            foreground=fg_text_dark,
            borderwidth=1,
            focusthickness=3,
            focuscolor=accent_color,
            relief="flat",
            padding=6,
            font=("Roboto", 11, "bold")
        )
        self.style.map("TButton",
            background=[('active', accent_color), ('disabled', '#f4f4f4')],
            foreground=[('active', fg_text_light), ('pressed', '#ffffff')],
            relief=[('pressed', 'sunken'), ('!pressed', 'flat')]
        )

        self.style.configure("Red.TButton",
            background=bg_light,  # start with sidebar color
            foreground=bg_error,
            borderwidth=1,
            focusthickness=3,
            focuscolor=bg_error,
            relief="flat",
            padding=2,
            font=("Roboto", 10, "bold")
        )
        self.style.map("Red.TButton",
            background=[('active', bg_light), ('disabled', '#f4f4f4')],
            foreground=[('active', bg_error), ('pressed', '#ffffff')],
            relief=[('pressed', 'sunken'), ('!pressed', 'flat')]
        )

        # Entries (input fields)
        self.style.configure("TEntry",
            fieldbackground=bg_light,
            foreground=fg_text_dark,
            background=accent_color,
            borderwidth=1,
            relief="flat",
            padding=4
        )

        # Checkbox
        self.style.configure("TCheckbutton",
            background=bg_dark,
            relief="flat",
            padding=2,
        )
        self.style.map("TCheckbutton",
            background=[('active', bg_dark), ('disabled', '#f4f4f4')],
        )

    def _set_light_theme(self):
        #? necessary when implementing theme switcher, but obviously out of scope
        pass
