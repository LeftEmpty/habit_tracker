import unittest
import sys, os
sys.path.append(os.path.abspath("."))

import db.controller as dbc
import obj.user as usr
import obj.habit as habit
import obj.subscription as sub


file = dbc.Connection.TEST

class TestObjectClasses(unittest.TestCase):
    """
    This would test object classes, i.e. User, HabitData, HabitSubscription, etc.
    They can only be partially tested via unit tests, following are a couple tests for the common basic functions of obj classes.
    More complex functionality is tested via request_test.

    #! To test objects themselves via unit tests i would have to either pass a test parameter
    #! to all functions that i want to test or work on the actual db, neither are good.
    #! E2E testing is possible via the provided pre-defined data.
    #! -> (populate_debug_data.py -> execute run.py with `--debug` argument) do test features themselves
    #! The functions that such an object would call are tested via the request_test.py file (request_handler functions)
    """
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        dbc.db_init(file)

        # Setup pre-reqs (these are tested in db_test.py)
        dbc.db_create_user("Tester", "testuser", "tester@example.com", "password", conn=file)
        dbc.db_create_habit_data(1, "Tester", "testhabit1", "this is a test", False, False, conn=file)
        dbc.db_create_habit_data(1, "Tester", "testhabit2", "this is also a test", False, False, conn=file)
        dbc.db_create_habit_sub(1, 1, "2000-1-1", None, "Daily", 0, 0, conn=file)
        dbc.db_create_habit_sub(1, 2, "2000-1-2", None, "Daily", 0, 0, conn=file)

    def test_create_user_obj_bool(self) -> None:
        result = dbc.db_get_user_by_id(1, conn=file)
        user = usr.User(
            user_id=result[0][0],
            display_name=result[0][1],
            username=result[0][2],
            email=result[0][3]
        )
        self.assertTrue(user.__bool__())

    def test_create_habitdata_obj_bool(self) -> None:
        result = dbc.db_get_habit_data_by_id(1, conn=file)
        data = habit.HabitData(
            name=result[0][1],
            desc=result[0][2],
            author_id=result[0][4],
            author_name=result[0][3],
            b_public=result[0][5],
            b_official=result[0][6],
            habit_id=result[0][0]
        )
        self.assertTrue(data.__bool__())

    def test_habitdata_obj_isregistered(self) -> None:
        result = dbc.db_get_habit_data_by_id(1, conn=file)
        data = habit.HabitData(
            name=result[0][1],
            desc=result[0][2],
            author_id=result[0][4],
            author_name=result[0][3],
            b_public=result[0][5],
            b_official=result[0][6],
            habit_id=result[0][0]
        )
        self.assertTrue(data.is_registered())

    @classmethod
    def tearDownClass(cls):
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None

if __name__ == '__main__':
    unittest.main()

