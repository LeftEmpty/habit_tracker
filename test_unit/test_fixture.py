import sqlite3
import hashlib
from db.src.database import Database
from typing import List
from util.src.data_classes import User

# additional conditional elements in GUI?
# commands?
# CLI?

def create_tables(db:Database) -> None:
    # @TODO create dummy data for 4 weeks for testing - auto generate this?
    pass
    # get db


def get_user_data():
    return User(
        0,
        "Max",
        hashlib.sha256("MaxTheGreatest".encode()).hexdigest(),
        hashlib.sha256("iam(not)secure".encode()).hexdigest(),
        "max.musterman@gmail.com",
        0
    )


def generate_test_user(user_data:User):
    """Creates a test users and adds them to the user table"""
    #? this should maybe be in global space to reduce stack memory usage on function call, or is it perma in memory?

    # @TODO return if check if the table exists
    # INSERT INTO...
        # user.stuff
        # User(
        #
        # )

    pass