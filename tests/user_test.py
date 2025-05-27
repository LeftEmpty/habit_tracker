import unittest
import sys, os
sys.path.append(os.path.abspath("."))

import db.controller as dbc
import obj.user as usr
import obj.request_handler as request

file = dbc.Connection.TEST

class TestUserObject(unittest.TestCase):
    """"""
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



    def test_create_user_object_bool(self) -> None:
        result = dbc.db_get_user_by_id(1, conn=file)
        user = usr.User(
            user_id=result[0][0],
            display_name=result[0][1],
            username=result[0][2],
            email=result[0][3]
        )
        self.assertTrue(user.__bool__())

    #! To test objects themselves via unit tests i would have to either pass a test parameter
    #! to all functions that i want to test or work on the actual db, neither are good.
    #! E2E testing is possible via the provided pre-defined data.
    #! -> (populate_debug_data.py -> execute run.py with `--debug` argument)

    # def test_user_get_subs(self) -> None:
    #     result = dbc.db_get_user_by_id(1, conn=file)
    #     user = usr.User(
    #         user_id=result[0][0],
    #         display_name=result[0][1],
    #         username=result[0][2],
    #         email=result[0][3]
    #     )
    #     result = user.get_subscribed_habits()
    #     self.assertEqual(len(result), 2)

    @classmethod
    def tearDownClass(cls):
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None


if __name__ == '__main__':
    unittest.main()

