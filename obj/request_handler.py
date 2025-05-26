import db.controller as dbc
import gui.util.validators as validator # validate_input_login, validate_input_register
from gui.util.gui_enums import InputResponse
from obj.subscription import HabitSubscription, Completion

import hashlib
from datetime import datetime, date

# forward declaring for better type checking / overview
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from gui.gui import GUI
    from obj.user import User
    from obj.habit import HabitData


#* **************************************** login / register ****************************************
def try_login_user(try_usr:str, try_pw:str, gui:"GUI") -> InputResponse:
    """Needs to receive valid infomration (checked in GUI - FrontScreen)
    Then hashes input, confirms login data, creates the user object and finally sets cur user in GUI

    Args:
        try_usr (str): valid username input
        try_pw (str): valid password input
        gui (GUI): owning GUI class reference, function sets cur_user here

    Returns:
        bool: returns true if login was successful
    """
    # validate input
    response = validator.validate_input_login(try_usr, try_pw)
    if response != InputResponse.SUCCESS:
        return response
    print(f"Log: trying login with valid input, usr: {try_usr}, pw: {try_pw}") #! remove this log in run environment

    hashed_pw = hashlib.sha256(try_pw.encode()).hexdigest()

    # fetch user data
    user_id:int = dbc.db_get_userid_by_credentials(try_usr, hashed_pw)
    if user_id == -1:
        return InputResponse.USR_NOTFOUND

    result = dbc.db_get_user_by_id(user_id)
    if len(result) <= 0:
        return InputResponse.USR_NOTFOUND

    # local import to avoid circular import # @TODO i dont like it
    from obj.user import User
    user = User(
        user_id=result[0][0],
        display_name=result[0][1],
        username=result[0][2],
        email=result[0][3]
    )
    if user != None:
        gui.cur_user = user
        user._on_login()
        # user.habit_subs = set(get_subs_for_user(user.user_id)) # now done in constructor
        return InputResponse.SUCCESS
    else:
        return InputResponse.DEFAULT

def try_register_user(try_email:str, try_usr:str, try_pw:str, try_pw2:str) -> InputResponse:
    """Needs to receive valid infomration (checked in GUI - FrontScreen)
    Then checks if user exists with given data exists, if it doesn't create user entry.

    ### @TODO
    Display name is set to username initially.. not great, probably better to ask for input or add a rand sufix, etc.

    Args:
        try_email (str): valid email input
        try_usr (str): valid username input
        try_pw (str): valid password input

    Returns:
        bool: success feedback
    """
    # validate input
    response = validator.validate_input_register(try_email, try_usr, try_pw, try_pw2)
    if response != InputResponse.SUCCESS:
        return response
    print(f"trying register with valid input, email: {try_email}, usr: {try_usr}, pw: {try_pw}, pw2: {try_pw2}") #! remove this log in run environment

    hashed_pw = hashlib.sha256(try_pw.encode()).hexdigest()

    if dbc.db_create_user(display_name=try_usr, username=try_usr, email=try_email, password=hashed_pw):
        response = InputResponse.SUCCESS
    else:
        response = InputResponse.DEFAULT
    return response


#* **************************************** user ****************************************
def get_user_displayname(user_id:int) -> str:
    result = dbc.db_get_user_by_id(user_id)
    if result[0][0]:
        return result[0][0]
    return ""


#* **************************************** habit ****************************************
def create_new_habit_via_data(owning_user:"User", habit_name:str, habit_desc:str, start_date:date, b_public:bool) -> Optional["HabitData"]:
        """Validates data and then calls dbc to create a habit

        Args:
            habit_name (str): name of habit to create
            habit_desc (str): description of habit to create
            b_public (bool): whether or not the habit should be public

        Returns:
            int: ID of the created habit data entry
        """

        return None

def create_new_habit_via_obj(data:"HabitData") -> int:
    """_summary_

    Args:
        data (HabitData): _description_

    Returns:
        int: ID of the created habit data entry
    """
    return dbc.db_create_habit_data(
        author_user_id=data.author_id,
        author_display_name=data.author_name,
        habit_name=data.name,
        habit_desc=data.desc,
        b_public=data.b_public,
        b_official=data.b_official,
        #last_modified=str(date.today())
    )

def modify_habit_data(habit:"HabitData") -> None:
    dbc.db_modify_habit_data(habit.id, habit.name, habit.desc, habit.b_public, str(habit.last_modified))

def get_habit_data(data_id:int) -> Optional["HabitData"]:
    """_summary_

    Args:
        data_id (int): _description_

    Returns:
        Optional[HabitData]: _description_
    """
    if data_id < 0: return None

    result = dbc.db_get_habit_data_by_id(data_id)
    if len(result) <= 0: return None

    # local import to avoid circular import # @TODO i dont like it
    from obj.habit import HabitData
    return HabitData(
        name=result[0][1],
        desc=result[0][2],
        author_id=result[0][4],
        author_name=result[0][3],
        b_public=result[0][5],
        b_official=result[0][6],
        habit_id=result[0][0]
    )

def get_all_public_habits() -> list["HabitData"]:
    result = dbc.db_get_public_habits()
    from obj.habit import HabitData
    habits:list[HabitData] = []
    for r in result:
        habits.append(HabitData(
            name=r[1],
            desc=r[2],
            author_id=r[4],
            author_name=r[3],
            b_public=r[5],
            b_official=r[6],
            habit_id=r[0]
        ))
    return habits

def get_habit_subs_count(habit_data_id:int) -> int:
    return dbc.db_get_subs_count_for_habit(habit_data_id)

def delete_habit_data_entry(habit_data_id:int) -> bool:
    return dbc.db_delete_habit_data(habit_data_id)


#* **************************************** subscriptions ****************************************
def create_new_sub_for_user(user_id:int, sub:HabitSubscription) -> int:
    """Creates a database entry for the provided habit subscription and returns its ID.

    Args:
        sub (HabitSubscription): Subscription object to save to DB.

    Returns:
        int: ID of the created entry.
    """
    id:int = dbc.db_create_habit_sub(
        user_id,
        sub.habit_data.id,
        str(sub.creation_date),
        None,
        sub.periodicity.value,
        sub.cur_streak,
        sub.max_streak
    )
    return id

def delete_habit_sub(sub_id:int) -> bool:
    return dbc.db_delete_habit_sub(sub_id)

def delete_habit_data(data_id:int) -> bool:
    return dbc.db_delete_habit_data(data_id)

#! DEPRECATED
#def modify_sub_periodicity(sub_id:int, new_periodicity:str) -> bool:
#    """modifies periodicty of subscription db entry."""
#    if sub_id < 0 or new_periodicity == "":
#        return False
#    return dbc.db_modifiy_sub_periodicty(sub_id, new_periodicity)

def update_sub_entry(sub:HabitSubscription) -> bool:
    """Modifies/Updates all mutable habit_subscription table entries.

    Args:
        sub (HabitSubscription): Object containing the updated data, used to overwrite existing data

    Returns:
        bool: success / failure
    """
    compl_date:str = sub.last_completed_date.isoformat() if sub.last_completed_date else ""
    dbc.db_modifiy_sub(
        sub_id=sub.id,
        periodicity=sub.periodicity.value,
        cur_streak=sub.cur_streak,
        max_streak=sub.max_streak,
        latest_date=compl_date
    )
    return False

def get_subs_for_user(user_id:int, user_displayname:str="") -> list[HabitSubscription]:
    """Uses dbc to query a habit subscription according to condition,
    then convert the resulting list into a list of HabitSubscription objects.

    Args:
        user_id (int): id of the user of which the subs are querried
        start_date (date): timeframe start - today, can be used to select subs that are due in a given timeframe

    Returns:
        list[HabitSubscription]: All subs that meet the requirements
    """
    # query db
    results = dbc.db_get_subs_for_user(user_id)
    if len(results) <= 0: return []

    # format query results
    subs:list[HabitSubscription] = []
    for r in results:
        sub = HabitSubscription(
            user_id=r[1],
            data_id=r[2],
            periodicity=r[3],
            cur_streak=r[4],
            max_streak=r[5],
            creation_date=r[6],
            last_completed_date=r[7],
            sub_id=r[0]
        )
        if sub:
            subs.append(sub)

    return subs

#* **************************************** completions ****************************************
def create_completion(completion:Completion) -> bool:
    """Format completion's date and try to create a DB enry.

    Args:
        completion (Completion): completion that should be added/registered to DB.

    Returns:
        bool: success / failure
    """
    date_str = completion.compl_date.isoformat()
    return dbc.db_create_completion(date_str, completion.user_id, completion.habit_sub_id)



def delete_completion(user_id:int, sub_id:int, date:date) -> bool:
    """deletes a completion based on the date.

    Args:
        user_id (int): owning user id.
        sub_id (int): owning sub id.
        date (date): date on which the completion should be deleted from.

    Returns:
        bool: success / failure
    """
    date_str = date.isoformat() # 'YYYY-MM-DD'
    return dbc.db_delete_completion(user_id, sub_id, date_str)

def delete_all_sub_completions_for_user(user_id:int, sub_id:int) -> bool:
    return dbc.db_delete_completion(user_id, sub_id, b_all=True)

def get_latest_sub_completion_for_user(user_id:int, sub_id:int) -> Optional[Completion]:
    result = dbc.db_get_latest_sub_completion_for_user(user_id, sub_id)
    if not len(result) > 0:
        return None
    c = Completion(
        user_id=result[0][1],
        habit_sub_id=result[0][2],
        compl_date=datetime.strptime(result[0][0], "%Y-%m-%d").date()
    )
    return c

def get_all_sub_completions_for_user(user_id:int, sub_id:int) -> list[Completion]:
    """Gets all completions that match user and sub IDs,
    then creates completion objects and return the elist.

    Args:
        user_id (int): owning user id.
        sub_id (_type_): owning sub id.

    Returns:
        list[Completion]: list of all completions that match the IDs, ERROR: list may be empty!
    """
    result = dbc.db_get_all_sub_completions_for_user(user_id, sub_id)
    if not len(result) > 0:
        return []
    completions:list[Completion] = []
    for r in result:
        completions.append(
            Completion(
                compl_date=datetime.strptime(r[0], "%Y-%m-%d").date(),
                user_id=r[1],
                habit_sub_id=r[2]
            )
        )
    return completions