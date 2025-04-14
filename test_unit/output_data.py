import os
from typing import List

# globals
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear') # clear console depending on os


def output_data_from_table(table:str, cond_id:int)->None:
    # @TODO get reference to db / client / server

    # @TODO get table via param name

    # @TODO query to select all and store in local var

    # @TODO output in understandable format

    pass

def output_user_data(user_id:int) -> None:
    """output all data relevant to a user, this includes habits and completions relevant to said user"""

    # @TODO get reference to db / client / server

    # @TODO output user data using output_data_from_table(user, user_id)

    # @TODO query user_habit table and store all id's

    # @TODO use the stored id's and output_data_from_table to output all habits stored by the user
    pass

def output_habit_data_for_user(user_id:int):
    """

    @return int: user id"""
    # @TODO get habit_list via user_id and store habit_ids

    # @TODO use output_data_from_table with these ids

    return []