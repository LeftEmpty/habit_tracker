from frontend.src.panels.panel import PanelBase
from frontend.src.data.habits import HabitSubscription, HabitData
import tkinter as tk
from tkinter import ttk
from typing import Optional


class ScrollableFrame(ttk.Frame):
    """ScrollableFrame class src: https://blog.teclado.com/tkinter-scrollable-frames/"""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, height=180, bg="#1E1E1E", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class HabitWidget(tk.Frame):
    def __init__(self, root, owning_habit_panel:PanelBase, habit_sub:HabitSubscription):
        super().__init__(self)
        self.config(bg="#000", height=24, pady=3) # match scrollable frame dimensions
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)

        # Create widgets
        habit_name_label = tk.Label(self, text=habit_sub.habit_data.name, bg='#000', fg="#fff", font=("Roboto", 12), anchor="w")
        self.habit_checkbox_btn = tk.Button(self, text="", fg='#fff', bg='#000', borderwidth=2, relief="flat", command=habit_sub.add_completion_event)
        self.habit_modify_btn = tk.Button(self, text="", fg='#fff', bg='#000', borderwidth=2, relief="flat", command=self.open_settings)

        # Layout widgets
        habit_name_label.grid(row=0, column=0, pady=8, sticky="w")
        self.habit_checkbox_btn.grid(row=0, column=1, pady=8, padx=8, sticky="e")
        self.habit_modify_btn.grid(row=0, column=2, pady=8, padx=8, sticky="e")

    def open_settings(self) -> None:
        """_summary_"""
        pass


class HabitsPanel(PanelBase):
    def __init__(self, root_gui, root_notebook:ttk.Notebook) -> None:
        super().__init__(root_gui, root_notebook)

    def setup_panel(self, panel_name:str = "Panel") -> None:
        super().setup_panel("Habits")
        if (self.root_gui.cur_user == None):
            # @TODO handle this error better, go back to login screen or something?
            return

        self.config(bg="#000")

        # Widgets
        self.list_title_label = tk.Label(self, text="Today's Habits", bg='#000', fg="#fff", font=("Roboto", 20), anchor="w")
        self.list_title_label.grid(row=0, column=0, pady=12)

        self.habit_list = ScrollableFrame(self)
        self.habit_list.grid(row=1, column=0, pady=24)

        habit_subs_list:list[HabitSubscription] = self.root_gui.cur_user.get_all_subscribed_habits()
        habit_widgets:list[HabitWidget] = []
        for hs in habit_subs_list:
            widget:HabitWidget = HabitWidget(self.habit_list.scrollable_frame, self, hs)
            habit_widgets.append(widget)

        self.add_habit_btn = tk.Button(self, text="Add Habit", fg='#fff', bg='#000', borderwidth=2, relief="flat", command=self.open_habit_pop_up)
        self.add_habit_btn.grid(row=2, column=0, pady=12)

    def open_habit_pop_up(self, habit_sub: Optional[HabitSubscription] = None) -> None:
        """Opens a pop up window to either ADD, EDIT or DELETE a habit

        Args:
            habit_sub (Optional[HabitSubscription], optional): _description_. Defaults to None.
        """
        HabitPopup(self, habit_sub)

    def try_create_habit(self) -> bool:
        return False

    def cancel(self) -> None:
        pass


class HabitPopup(tk.Toplevel):
    def __init__(self, parent, habit_sub:Optional[HabitSubscription] = None):
        super().__init__(parent)
        title = "Add Habit" if habit_sub is None else "Edit Habit"
        self.title(title)
        self.geometry('2800x360')
        self.config(bg="#000")
        self.habit_sub = habit_sub

        # Widgets
        self.title_label = tk.Label(self, text=title, bg='#000', fg="#fff", font=("Roboto", 28), anchor="w")
        self.name_label = tk.Label(self, text="Name", bg='#000', fg="#fff", font=("Roboto", 13), anchor="w")
        self.name_entry = tk.Entry(self)
        self.desc_label = tk.Label(self, text="Description", bg='#000', fg="#fff", font=("Roboto", 13), anchor="w")
        self.desc_entry = tk.Text(self, height=4, width=30)
        self.create_button = tk.Button(self, text="Create", fg='#fff', bg='#000', borderwidth=2, relief="flat", command=self.try_create_or_update_habit)
        self.cancel_button = tk.Button(self, text="Cancel", fg='#fff', bg='#000', borderwidth=2, relief="flat", command=self.destroy)
        self.delete_button = tk.Button(self, text="Cancel", fg='#fff', bg='#000', borderwidth=2, relief="flat", command=self.try_delete_habit)

        # Pre-fill if editing
        if habit_sub:
            self.name_entry.insert(0, habit_sub.habit_data.name)
            self.desc_entry.insert("1.0", habit_sub.habit_data.desc)

        # Layout
        self.title_label.pack()
        self.name_label.pack()
        self.name_entry.pack()
        self.desc_label.pack()
        self.desc_entry.pack()
        self.cancel_button.grid(row=5, pady=12)
        self.create_button.grid(row=5, pady=12)
        # self.title_label.grid(row=0, column=0, columnspan=2, pady=8, padx=8, sticky="w")
        # self.name_label.grid(row=1, column=0, padx=8, sticky="w")
        # self.name_entry.grid(row=1, column=1, columnspan=2)
        # self.desc_label.grid(row=2, column=0, padx=8, sticky="w")
        # self.desc_entry.grid(row=2, column=1, columnspan=2)
        # self.cancel_button.grid(row=3, column=0, pady=12)
        # self.create_button.grid(row=3, column=1, pady=12)

    def try_create_or_update_habit(self) -> None:
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get("1.0", "end").strip()
        if not name:
            print("Name required")
            return
        if self.habit_sub:
            print(f"Updating habit: {name} - {desc}")
            # @TODO call action handler
        else:
            print(f"Creating new habit: {name} - {desc}")
            # @TODO call action handler
        self.destroy()

    def try_delete_habit(self) -> None:
        name = self.name_entry.get().strip()
        print(f"Deleting the habit: {name}")
        pass
