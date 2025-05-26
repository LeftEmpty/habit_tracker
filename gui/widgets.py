import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable, Dict

from gui.util.gui_enums import InputResponse, HabitListMode, HabitQueryCondition
from obj.habit import HabitData
from obj.subscription import HabitSubscription, Periodicity

# forward declaring for better type checking / overview
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui import GUI
    from obj.user import User


class ScrollableFrame(ttk.Frame):
    """ScrollableFrame class src: https://blog.teclado.com/tkinter-scrollable-frames/"""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, height=380, width=520, bg="#1E1E1E", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)
        self.scrollable_frame.config(pady=2, padx=4, bg="#1E1E1E")
        self.scrollable_frame.columnconfigure(0, weight=1)

        # Bind the scrollable frame to the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, width=520, anchor="nw")

        # Configure canvas to expand
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


class HabitSubListWidget(ttk.Frame):
    def __init__(self, parent:ttk.Frame, owning_gui:"GUI", mode:HabitListMode, habits:Optional[list[HabitData]]=None, subs:Optional[list[HabitSubscription]] = None):
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

        self.owning_gui = owning_gui
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
                    widget = SubWidget(self, self.owning_gui, s)
                    widget.pack(fill="x", pady=2, expand=True)
        else:
            if self.habits and len(self.habits) > 0:
                for h in self.habits:
                    widget = HabitWidget(self, self.owning_gui, h)
                    widget.pack(fill="x", pady=2)

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
                self.subs = self.owning_user.get_subscribed_habits(HabitQueryCondition.RELEVANT_TODAY)
        else:
            if self.owning_user:
                self.habits = self.owning_user.get_all_non_subbed_public_habits()

        # destroy old widgets
        print ("HabistSubList is being re-populated due to refresh.")
        for widget in self.container.scrollable_frame.winfo_children():
            widget.destroy()

        # repopulate widgets
        self._populate_list()


class HabitWidget(ttk.Frame):
    def __init__(self, parent_list:HabitSubListWidget, owning_gui:"GUI", data:HabitData):
        """List item for HabitSubListWidget.
        Widget for a single habit subscription entry in a HabitListWidget.

        Args:
            parent_list (HabitSubListWidget): Owning list widget.
            owning_gui (GUI): root gui of this app.
            sub (HabitSubscription): habit sub that is represented by this widget.
        """
        super().__init__(parent_list.container.scrollable_frame)

        self.config(style="Sidebar.TFrame")
        self.columnconfigure(0, weight=8)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.parent_list = parent_list
        self.owning_gui = owning_gui
        self.data = data

        self._build_ui()

    def _build_ui(self) -> None:
        """Build basic widget layout"""
        self.name_label = ttk.Label(self, text=self.data.name, style="Sidebar.TLabel")
        self.name_label.grid(row=0, column=0, padx=8, pady=8, sticky="w")

        desc = self.data.desc if len(self.data.desc) < 25 else str(self.data.desc[:25] + "..")
        self.desc_label = ttk.Label(self, text=f"-> {desc}", style="Sidebar.TLabel", font=("TkDefaultFont", 10, "italic"))
        self.desc_label.grid(row=1, column=0, padx=8, pady=8, sticky="w")

        self.sub_btn:ttk.Button = ttk.Button(self, text="[+]", command=self._subscribe)
        self.sub_btn.grid(row=0, column=2, pady=4, padx=8, sticky="e")

        self.periodicity_var = tk.StringVar()
        self.periodicity_menu = ttk.Combobox(self, textvariable=self.periodicity_var, state="readonly")
        self.periodicity_menu['values'] = [p.value for p in Periodicity]
        self.periodicity_menu.grid(row=1, column=1, columnspan=2, padx=8, pady=8, sticky="e")

    def _subscribe(self):
        """Type check periodicity, then create new subscription based on this widgets habit data for the current user.
        Finally on success, update the user's subscribed habits and reload the parent list."""
        if not self.periodicity_var.get():
            self.owning_gui.give_input_feedback(InputResponse.NO_PERIODICITY)
            return

        if self.data and self.owning_gui.cur_user:
            new_sub:HabitSubscription = HabitSubscription(
                user_id=self.owning_gui.cur_user.user_id,
                data_id=self.data.id,
                periodicity=self.periodicity_var.get(),
                cur_streak=0,
                max_streak=0,
                last_completed_date=None
            )
            if new_sub:
                self.owning_gui.cur_user.update_subscribed_habits()
                self.parent_list.reload_list()


class SubWidget(ttk.Frame):
    def __init__(self, parent_list:HabitSubListWidget, owning_gui:"GUI", sub:HabitSubscription):
        """List item for HabitSubListWidget.
        Widget for a single habit subscription entry in a HabitListWidget.

        Args:
            parent_list (HabitSubListWidget): Owning list widget.
            owning_gui (GUI): root gui of this app.
            sub (HabitSubscription): habit sub that is represented by this widget.
        """
        super().__init__(parent_list.container.scrollable_frame)

        self.config(style="Sidebar.TFrame")
        self.columnconfigure(0, weight=8)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.parent_list = parent_list
        self.owning_gui = owning_gui
        self.sub = sub

        self._build_ui()
        self._update_state(self.sub.get_completed_state())

    def _build_ui(self) -> None:
        """Build basic widget layout"""
        self.name_label = ttk.Label(self, text=self.sub.habit_data.name, style="Sidebar.TLabel")
        self.name_label.grid(row=0, column=0, pady=8, sticky="w")

        self.compl_btn:ttk.Button = ttk.Button(self, text="[ ]", command=self.complete)
        self.compl_btn.grid(row=0, column=1, pady=4, padx=4, sticky="e")

        ttk.Button(self, text="", command=self.edit).grid(row=0, column=2, pady=4, padx=4, sticky="e")

    def _update_state(self, compl:bool) -> None:
        """Adjusts widget configuration based on habit completion state."""
        if compl:
            self.compl_btn.config(text="[✗]")
            self.config(style="NotificationSuccess.TFrame")
            self.name_label.config(style="NotificationSuccess.TLabel")
        else:
            self.compl_btn.config(text="[✓]")

    def complete(self):
        """Call on_completion_input_action on this wigdet's subscription, then update states and refresh parent list."""
        if not self.sub:
            return
        self.sub.on_completion_input_action()
        self._update_state(self.sub.get_completed_state())
        self.parent_list.reload_list()

    def edit(self):
        """Opens HabitEditPopup after null-checking, only allows action if current user is author of habit."""
        if self.sub and self.owning_gui.cur_user:
            b_is_author:bool = self.owning_gui.cur_user.user_id == self.sub.habit_data.author_id
            HabitEditPopup(self.owning_gui, self.owning_gui.cur_user, self.sub, b_is_author,self.parent_list.reload_list)
        elif self.owning_gui:
            self.owning_gui.give_input_feedback(InputResponse.NOT_AUTHOR)


class HabitEditPopup(tk.Toplevel):
    def __init__(self, root_gui:"GUI", user:"User", sub:HabitSubscription, b_is_author:bool, on_creation_callback:Callable[[], None]):
        """Popup window Widget used to enter habit subscriptions.

        Args:
            root_gui (GUI): _description_
            user (User): _description_
            sub (HabitSubscription): _description_
            b_is_author (bool): user currently editing is author of habit.
            on_save (_type_, optional): _description_. Defaults to None.
        """
        if not user or not root_gui:
            self.destroy()
        super().__init__(root_gui.root)

        self.title("Edit Habit")
        self.geometry("480x480")

        self.root_gui = root_gui
        self.user = user
        self.habit_data = sub.habit_data
        self.sub = sub
        self.on_creation_callback = on_creation_callback

        self._init_vars()
        self._build_ui(b_is_author)

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

    def _build_ui(self, b_author_ui:bool):
        frame = ttk.Frame(self, padding=22, style="ContentArea.TFrame")
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)

        if b_author_ui:
            ttk.Label(frame, text="Edit Habit", font=("TkDefaultFont", 22, "bold")).grid(pady=16, row=0, column=0, columnspan=3, sticky="w")

            ttk.Label(frame, text="Habit Name").grid(row=1, column=0, sticky="w")
            self.name_entry = ttk.Entry(frame, textvariable=self.name_var)
            self.name_entry.grid(row=1, column=1, columnspan=2, pady=8, sticky="ew")

            ttk.Label(frame, text="Description").grid(row=2, column=0, sticky="w")
            self.desc_entry = ttk.Entry(frame, textvariable=self.desc_var)
            self.desc_entry.grid(row=2, column=1, columnspan=2, pady=8, sticky="ew")

            ttk.Label(frame, text="Public").grid(row=3, column=0, sticky="w")
            self.public_check = ttk.Checkbutton(frame, variable=self.public_var)
            self.public_check.grid(row=3, column=1, pady=8, sticky="ew")

            #! LEGACY - removed periodicity editing for now
            #ttk.Label(frame, text="Periodicity").grid(row=4, column=0, sticky="w")
            #self.periodicity_menu = ttk.Combobox(frame, textvariable=self.periodicity_var, state="readonly")
            #self.periodicity_menu['values'] = [p.value for p in Periodicity]
            #self.periodicity_menu.grid(row=4, column=1, columnspan=2, pady=8, sticky="ew")

            ttk.Label(frame, text="Periodicity: ").grid(row=4, column=0, sticky="w")
            ttk.Label(frame, text=f"[{self.sub.periodicity.value}].").grid(row=4, column=1, columnspan=2, pady=8, sticky="w")
            ttk.Label(frame, text="Editing periodicity is currently not supported.", font=("TkDefaultFont", 10, "italic"))\
                .grid(row=5, column=0, columnspan=3, sticky="w")

            self.save_btn = ttk.Button(frame, text="Save", command=self._on_save)
            self.save_btn.grid(row=6, column=0, padx=8, pady=18)
            self.delete_btn = ttk.Button(frame, text="Delete", command=self._on_delete)
            self.delete_btn.grid(row=6, column=1, padx=8, pady=18)
            self.cancel_btn = ttk.Button(frame, text="Cancel", command=self.destroy)
            self.cancel_btn.grid(row=6, column=2, padx=8, pady=18)

        else:
            ttk.Label(frame, text="Delete Habit?", font=("TkDefaultFont", 22, "bold")).grid(pady=16, row=0, column=0, columnspan=3, sticky="w")

            ttk.Label(frame, text=f"Habit Name: {self.sub.habit_data.name}").grid(row=1, column=0, columnspan=3, sticky="w")
            ttk.Label(frame, text=f"Habit Desc: {self.sub.habit_data.desc}").grid(row=2, column=0, columnspan=3, sticky="w")
            ttk.Label(frame, text=f"Periodicity: {self.sub.periodicity.value}").grid(row=3, column=0, columnspan=3, sticky="w")

            ttk.Label(frame, text=f"Author: {self.sub.habit_data.author_name}").grid(row=4, column=0, columnspan=3, sticky="w")
            ttk.Label(frame, text="Cannot edit a habit you didn't author.", font=("TkDefaultFont", 10, "italic"))\
                .grid(row=5, column=0, columnspan=3, sticky="w")

            self.delete_btn = ttk.Button(frame, text="Delete", command=self._on_delete)
            self.delete_btn.grid(row=6, column=0, padx=8, pady=18)
            self.cancel_btn = ttk.Button(frame, text="Cancel", command=self.destroy)
            self.cancel_btn.grid(row=6, column=2, padx=8, pady=18)

        frame.columnconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)

    def _on_delete(self):
        """Cancels the subscription (might delete it, logic handled in sub) and updates users sub list.
        Then calls callback to list, gives feedback, and destroys self(popup)"""
        self.sub.on_cancel_subscription()
        self.user.update_subscribed_habits()

        if self.on_creation_callback:
            self.on_creation_callback()
            self.root_gui.give_input_feedback(InputResponse.SUCCESS)

        self.destroy()

    def _on_save(self):
        """Saves / Modifies subscription & data objects & db entries."""
        # Update existing HabitData
        if self.habit_data is None or self.sub is None: return

        # Validate input
        if self.name_entry.get() == "" or self.desc_entry == "": #or self.periodicity_var == tk.StringVar():
            self.root_gui.give_input_feedback(InputResponse.EMPTY_FIELDS)

        # Update sub & data
        self.habit_data.modify_data(
            new_name=self.name_var.get(),
            new_desc=self.desc_var.get(),
            b_public=self.public_var.get()
        )
        #self.sub.modify_sub(self.periodicity_var.get())

        self.user.update_subscribed_habits()

        # Callback to home screen - habitlist to get it to reload/refresh
        if self.on_creation_callback:
            self.on_creation_callback()
            self.root_gui.give_input_feedback(InputResponse.SUCCESS)

        self.destroy()


class HabitCreationPopup(tk.Toplevel):
    def __init__(self, root_gui:"GUI", user:"User", on_creation_callback:Callable[[], None]):
        """"""
        if not user or not root_gui:
            self.destroy()
        super().__init__(root_gui.root)

        self.root_gui = root_gui
        self.user = user
        self.on_creation_callback = on_creation_callback

        self.title("Create Habit")
        self.geometry("480x480")

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding=22, style="ContentArea.TFrame")
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)

        ttk.Label(frame, text="Create Habit", font=("TkDefaultFont", 22, "bold")).grid(pady=16, row=0, column=0, columnspan=3, sticky="w")

        ttk.Label(frame, text="Habit Name").grid(row=1, column=0, sticky="w")
        self.name_entry = ttk.Entry(frame)
        self.name_entry.grid(row=1, column=1, pady=8, sticky="ew")

        ttk.Label(frame, text="Description").grid(row=2, column=0, sticky="w")
        self.desc_entry = ttk.Entry(frame)
        self.desc_entry.grid(row=2, column=1, pady=8,sticky="ew")

        self.is_public = tk.BooleanVar()
        ttk.Label(frame, text="Public").grid(row=3, column=0, sticky="w")
        self.public_check = ttk.Checkbutton(frame, variable=self.is_public)
        self.public_check.grid(row=3, column=1, pady=8, sticky="w")

        ttk.Label(frame, text="Periodicity").grid(row=4, column=0, sticky="w")
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
        # Validate input
        if self.name_entry.get() == "" or self.desc_entry == "" or not self.periodicity_var.get():
            self.root_gui.give_input_feedback(InputResponse.EMPTY_FIELDS)
            return

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

        self.destroy()


class PeriodicityHabitListPopup(tk.Toplevel):
    def __init__(self, root_gui:"GUI", subs:list[HabitSubscription]):
        """"""
        super().__init__(root_gui.root)

        self.root_gui = root_gui
        self.subs = subs

        self.title("Habit Periodicity List")
        self.geometry("600x600")

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding=22, style="ContentArea.TFrame")
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)

        ttk.Label(frame, text="Habit Periodicity List", font=("TkDefaultFont", 18, "bold")).pack(pady=4)

        container:ScrollableFrame = ScrollableFrame(frame)
        container.pack(fill='both', anchor='center')

        ttk.Label(container.scrollable_frame, text="-- DAILY --",  anchor='center', font=("TkDefaultFont", 16, "bold")).pack(fill='x', pady=2)
        self.container_daily:ttk.Frame = ttk.Frame(container.scrollable_frame, padding=12, style="Sidebar.TFrame")
        self.container_daily.pack(fill='x')
        ttk.Label(container.scrollable_frame, text="-- WEEKLY --",  anchor='center', font=("TkDefaultFont", 16, "bold")).pack(fill='x', pady=2)
        self.container_weekly:ttk.Frame = ttk.Frame(container.scrollable_frame, padding=12, style="Sidebar.TFrame")
        self.container_weekly.pack(fill='x')
        ttk.Label(container.scrollable_frame, text="-- MONDAYS --",  anchor='center', font=("TkDefaultFont", 16, "bold")).pack(fill='x', pady=2)
        self.container_mon:ttk.Frame = ttk.Frame(container.scrollable_frame, padding=12, style="Sidebar.TFrame")
        self.container_mon.pack(fill='x')
        ttk.Label(container.scrollable_frame, text="-- TUESDAYS --",  anchor='center', font=("TkDefaultFont", 16, "bold")).pack(fill='x', pady=2)
        self.container_tue:ttk.Frame = ttk.Frame(container.scrollable_frame, padding=12, style="Sidebar.TFrame")
        self.container_tue.pack(fill='x')
        ttk.Label(container.scrollable_frame, text="-- WEDNESDAYS --",  anchor='center', font=("TkDefaultFont", 16, "bold")).pack(fill='x', pady=2)
        self.container_wed:ttk.Frame = ttk.Frame(container.scrollable_frame, padding=12, style="Sidebar.TFrame")
        self.container_wed.pack(fill='x')
        ttk.Label(container.scrollable_frame, text="-- THURSDAYS --",  anchor='center', font=("TkDefaultFont", 16, "bold")).pack(fill='x', pady=2)
        self.container_thu:ttk.Frame = ttk.Frame(container.scrollable_frame, padding=12, style="Sidebar.TFrame")
        self.container_thu.pack(fill='x')
        ttk.Label(container.scrollable_frame, text="-- FRIDAYS --",  anchor='center', font=("TkDefaultFont", 16, "bold")).pack(fill='x', pady=2)
        self.container_fri:ttk.Frame = ttk.Frame(container.scrollable_frame, padding=12, style="Sidebar.TFrame")
        self.container_fri.pack(fill='x')
        ttk.Label(container.scrollable_frame, text="-- SATURDAYS --",  anchor='center', font=("TkDefaultFont", 16, "bold")).pack(fill='x', pady=2)
        self.container_sat:ttk.Frame = ttk.Frame(container.scrollable_frame, padding=12, style="Sidebar.TFrame")
        self.container_sat.pack(fill='x')
        ttk.Label(container.scrollable_frame, text="-- SUNDAYS --",  anchor='center', font=("TkDefaultFont", 16, "bold")).pack(fill='x', pady=2)
        self.container_sun:ttk.Frame = ttk.Frame(container.scrollable_frame, padding=12, style="Sidebar.TFrame")
        self.container_sun.pack(fill='x')


        # Add widgets to appropriate container via periodicity
        container_dict:Dict[Periodicity, ttk.Frame] = {
            Periodicity.DAILY : self.container_daily,
            Periodicity.WEEKLY : self.container_weekly,
            Periodicity.MONDAY : self.container_mon,
            Periodicity.TUESDAY : self.container_tue,
            Periodicity.WEDNESDAY : self.container_wed,
            Periodicity.THURSDAY : self.container_thu,
            Periodicity.FRIDAY : self.container_fri,
            Periodicity.SATURDAY : self.container_sat,
            Periodicity.SUNDAY : self.container_sun
        }
        for s in self.subs:
            ttk.Label(container_dict[s.periodicity], text=f"Habit: {s.habit_data.name}\nDesc: {s.habit_data.desc}\nAuthor: {s.habit_data.author_name}").pack(fill='x', pady=4)

        ttk.Button(frame, text="Close", command=self.destroy).pack(fill='x', pady=12)

        self.columnconfigure(1, weight=1)