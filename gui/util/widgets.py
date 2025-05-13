import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable

from gui.util.gui_enums import InputResponse, HabitListMode
from obj.src.habit import HabitData
from obj.src.subscription import HabitSubscription, Periodicity

# forward declaring for better type checking / overview
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.src.gui import GUI
    from obj.src.user import User


class ScrollableFrame(ttk.Frame):
    """ScrollableFrame class src: https://blog.teclado.com/tkinter-scrollable-frames/"""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, height=380, bg="#1E1E1E", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.columnconfigure(0, weight=1)

        # Bind the scrollable frame to the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Configure canvas to expand
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class HabitSubListWidget(ttk.Frame):
    def __init__(self, parent:ttk.Frame, owning_gui:"GUI", mode:HabitListMode, habits:Optional[list[HabitData]] = None, subs:Optional[list[HabitSubscription]] = None):
        """creates a scrollable frame and inserts the habits (data) as a list of habit wigets"""
        super().__init__(parent, style="Sidebar.TFrame")
        self.container:ScrollableFrame = ScrollableFrame(self)
        self.container.pack(fill='both')

        if (habits is not None and subs is not None) or (habits is None and subs is None):
            #raise ValueError("Pass exactly one list of habits or subs (1 empty list).")
            return

        self.widgets = []
        self.cur_mode:HabitListMode = mode
        self.subs = subs
        self.habits = habits

        self.owning_user:User|None = owning_gui.cur_user

        self._populate_list()

    def _populate_list(self) -> None:
        """populates list, used display the sub / habit widgets in the scrollable frame.
        Initially populates the list with provided subs during construction.

        Args:
            new_subs_list (list, optional): Updated list of widgets to show. Defaults to [].
        """
        if self.cur_mode == HabitListMode.SUB:
            if self.subs and len(self.subs) > 0:
                for s in self.subs:
                    widget = SubWidget(self, s)
                    widget.pack(fill="x", pady=2, expand=True)
        else:
            # @TODO
            if self.habits and len(self.habits) > 0:
                for h in self.habits:
                    #widget = SubWidget(self, h)
                    #widget.pack(fill="x", pady=2)
                    pass

    def reload_list(self) -> None:
        """Used to update / refresh the list after construction.
        Deletes all 'child' widgets of self.container.scrollable_frame,
        then repopulates the list with the updated list.

        Args:
            new_subs_list (list, optional): _description_. Defaults to [].
        """
        # update widget list
        if self.cur_mode == HabitListMode.SUB:
            if self.owning_user:
                self.subs = self.owning_user.habit_subs
        else:
            # @TODO
            pass

        # destroy old widgets
        for widget in self.container.scrollable_frame.winfo_children():
            print ("habist sub list, sub widget being destoryed due to refresh: " + widget.winfo_name())
            widget.destroy()

        # repopulate widgets
        self._populate_list()


class SubWidget(ttk.Frame):
    def __init__(self, parent:HabitSubListWidget, sub:HabitSubscription):
        """List item for HabitSubListWidget.
        Widget for a single habit subscription entry in a HabitListWidget.

        Args:
            parent (HabitSubListWidget): Owning list widget.
            sub (HabitSubscription): habit sub that is represented by this widget.
        """
        super().__init__(parent.container.scrollable_frame)

        self.config(style="Sidebar.TFrame")
        self.columnconfigure(0, weight=8)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.parent = parent
        self.sub = sub

        # Habit name
        ttk.Label(self, text=sub.habit_data.name, style="Sidebar.TLabel").grid(row=0, column=0, pady=8, sticky="w")

        # Adjust buttons based on subscription bool (either settings popup, or add subscribe button)
        btn_ico:str = ""
        if sub.get_completed_state():
            btn_ico = ""
        self.compl_btn:ttk.Button = ttk.Button(self, text=btn_ico, command=self.complete)
        self.compl_btn.grid(row=0, column=1, pady=4, padx=4, sticky="e")

        ttk.Button(self, text="", command=self.edit).grid(row=0, column=2, pady=4, padx=4, sticky="e")

    def complete(self):
        if self.sub:
            if self.sub.completed_locally:
                self.sub.add_completion_event()
                self.sub.completed_locally = True
                self.compl_btn.config(text="")
            else:
                self.sub.completed_locally = False
        # @TODO would be better if it first only completes it locally and on close/disconnect adds the completion event
        # @TODO issue with that would be crashes, etc. but maybe that could be considered an expected error? idk
        # self.parent.reload_list()

    def edit(self):
        if self.sub:
            HabitEditPopup(self, self.sub)


class HabitEditPopup(tk.Toplevel):
    def __init__(self, parent, sub:HabitSubscription, on_save=None):
        """Used to either create or edit subscriptions, edit mode updates data, creating inits a new HabitData obj and auto-subs to it

        Args:
            parent (_type_): parent widget this popup is spawned from
            user (User): _description_
            mode (str, optional): Determines popup mode, needs to be either 'create' or 'edit'. Defaults to 'create'.
            habit_data (_type_, optional): _description_. Defaults to None.
            subscription (_type_, optional): _description_. Defaults to None.
            on_save (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(parent)

        # self.title("Habit Editor" if mode == 'edit' else "Create Habit")
        self.title("Create Habit")
        self.habit_data = sub.habit_data
        self.sub = sub
        self.on_save = on_save

        self._init_vars()
        self._build_ui()

    def _init_vars(self):
        # Fill in with defaults or existing values
        self.name_var = tk.StringVar(value=self.habit_data.name if self.habit_data else "")
        self.desc_var = tk.StringVar(value=self.habit_data.desc if self.habit_data else "")
        self.public_var = tk.BooleanVar(value=self.habit_data.b_public if self.habit_data else False)

        self.periodicity_var = tk.StringVar()
        if self.sub:
            self.periodicity_var.set(self.sub.periodicity.value)
        else:
            self.periodicity_var.set(Periodicity.DAILY.value)

    def _build_ui(self):
        """Internal/private function to build the UI widgets."""
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Habit Name").grid(row=0, column=0, sticky="w")
        name_entry = ttk.Entry(frame, textvariable=self.name_var)
        name_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame, text="Description").grid(row=1, column=0, sticky="w")
        desc_entry = ttk.Entry(frame, textvariable=self.desc_var)
        desc_entry.grid(row=1, column=1, sticky="ew")

        public_check = ttk.Checkbutton(frame, text="Public Habit", variable=self.public_var)
        public_check.grid(row=2, columnspan=2, sticky="w")

        ttk.Label(frame, text="Periodicity").grid(row=3, column=0, sticky="w")
        periodicity_menu = ttk.Combobox(frame, textvariable=self.periodicity_var, state="readonly")
        periodicity_menu['values'] = [p.value for p in Periodicity]
        periodicity_menu.grid(row=3, column=1, sticky="ew")

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Save Changes", command=self._on_save).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side="left", padx=5)

        frame.columnconfigure(1, weight=1)

    def _on_save(self):
        """"""
        # Update existing HabitData
        if self.habit_data is None or self.sub is None: return
        self.habit_data.update_data(
            new_name=self.name_var.get(),
            new_desc=self.desc_var.get(),
            b_public=self.public_var.get()
        )
        # Update subscription periodicity
        self.sub.periodicity = Periodicity(self.periodicity_var.get())

        if self.on_save:
            self.on_save(self.habit_data, self.sub.periodicity)
        self.destroy()


class HabitCreationPopup(tk.Toplevel):
    def __init__(self, root_gui:"GUI", user:"User", on_creation_callback:Callable[[], None]):
        """"""
        super().__init__(root_gui.root)
        if not user or not root_gui:
            self.destroy()

        self.root_gui = root_gui
        self.user = user
        self.on_creation_callback = on_creation_callback

        self.title("Create Habit")
        self.geometry("480x480")

        frame = ttk.Frame(self, padding=22, style="ContentArea.TFrame")
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)

        ttk.Label(frame, text="Create Habit", font=("TkDefaultFont", 22, "bold")).grid(row=0, column=0, sticky="w")

        ttk.Label(frame, text="Habit Name").grid(row=1, column=0, sticky="w")
        self.name_entry = ttk.Entry(frame)
        self.name_entry.grid(row=1, column=1, pady=8, sticky="ew")

        ttk.Label(frame, text="Description").grid(row=2, column=0, sticky="w")
        self.desc_entry = ttk.Entry(frame)
        self.desc_entry.grid(row=2, column=1, pady=8,sticky="ew")

        self.is_public = tk.BooleanVar()
        ttk.Label(frame, padding=8, text="Public").grid(row=3, column=0, sticky="w")
        self.public_check = ttk.Checkbutton(frame, variable=self.is_public)
        self.public_check.grid(row=3, column=1, pady=8, sticky="w")

        ttk.Label(frame, padding=8, text="Periodicity").grid(row=4, column=0, sticky="w")
        self.periodicity_var = tk.StringVar()
        self.periodicity_menu = ttk.Combobox(frame, textvariable=self.periodicity_var, state="readonly")
        self.periodicity_menu['values'] = [p.value for p in Periodicity]
        self.periodicity_menu.grid(row=4, column=1, pady=8, sticky="ew")

        self.create_btn = ttk.Button(frame, text="Create", command=self._on_save)
        self.create_btn.grid(row=5, column=0, padx=8, pady=18)
        self.cancel_btn = ttk.Button(frame, text="Cancel", command=self.destroy)
        self.cancel_btn.grid(row=5, column=1, padx=8, pady=18)

        self.columnconfigure(1, weight=1)

    def _on_save(self):
        """Creates HabitData and HabitSubscription objects via the input entry fields. (Validates data first)
        Both objects register themselves to the DB.
        Finally refreshes widget list on home screen and destroys itself."""
        # @TODO i don't like that this logic is in a widget class, might be better to move this to e.g. gui_events

        # Validate input
        if self.name_entry.get() == "" or self.desc_entry == "":
            self.root_gui.give_input_feedback(InputResponse.EMPTY_FIELDS)

        # Create & register HabitData obj
        data:HabitData = HabitData(
            name=self.name_entry.get(),
            desc=self.desc_entry.get(),
            author_id=self.user.user_id,
            b_public=self.is_public.get(),
            b_official=False,
            author_name=self.user.display_name
        ) # registers self in constructor
        if not data.is_registered():
            return

        # Create & register HabitSub
        sub = HabitSubscription(
            user_id=self.user.user_id,
            data_id=data.id,
            periodicity=Periodicity(self.periodicity_var.get()),
            cur_streak=0,
            max_streak=0,
            last_completed_date=None,
            habit_data=data
        ) # registers self in constructor
        if not sub.is_registered():
            # @TODO test this delete zombie habit data entry created above
            return

        self.user.habit_subs.append(sub)

        # Callback to home screen - habitlist to get it to reload/refresh
        if self.on_creation_callback:
            self.on_creation_callback()
            self.root_gui.give_input_feedback(InputResponse.SUCCESS)

        # Upload HabitSub, Reload habitlist on home screen
        self.destroy()

