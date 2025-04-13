from dataclasses import dataclass
from util.src.data_classes.data_structs import Periodicty

#* general data flow is as follows:
#* GUI (user-aware) ➜ ActionHandler (user-aware) ➜ DataBase (has connection & user_id passed in queries)

@dataclass
class Periodicty:
    # Timeframe (in hours)
    timeframe: int
    # Frequency (in hours)
    frequency: int

@dataclass
class Habit:
    id: int
    user_id: int
    name: str
    description: str
    periodicty: Periodicty

@dataclass
class HabitList:
    last_updated_on: str
    streak: int
    highest_streak: int
    user_id: int
    habit_id: int

@dataclass
class User:
    user: str
    display_name: str
    username: str # hashed
    password: str # hashed
    habit_list: HabitList