from db.src.database import Database
from typing import List

# screen in GUI?
# commands?
# CLI?

def create_test_fixture(db:Database) -> None:
    # @TODO create dummy data for 4 months for testing - auto generate this?
    pass


def generate_test_user():
    #? this should maybe be in global space to reduce stack memory usage on function call, or is it perma in memory?
    display_base:list[str] = ["Antron", "Berta", ""]
    display_prefix:list[str] = ["Hi", "x", ""]
    display_suffix:list[str] = ["", "", ""]

    # @TODO generate random display & username

    email_provider:list[str] = ["gmail.com", "web.de", "yahoo.jp.co", "outlook.com", "gmx.net"]
    pass