from dataclasses import dataclass

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
    user_id: int
    display_name: str
    username: str # hashed
    password: str # hashed
    email: str
    habit_list_id: int #HabitList