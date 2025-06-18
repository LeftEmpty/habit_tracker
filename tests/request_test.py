import unittest
import sys, os
sys.path.append(os.path.abspath("."))

from datetime import date, timedelta

import db.controller as dbc
import obj.request_handler as request
import obj.subscription as sub
import obj.habit as data

file = dbc.Connection.TEST


#* ********************************************* User *********************************************
class TestUserSpecificRequests(unittest.TestCase):
    """"""
    @classmethod
    def setUpClass(cls) -> None:
        os.remove(file.value) if os.path.exists(file.value) else None
        dbc.db_init(file)

        # Setup pre-reqs (these are tested in db_test.py)
        dbc.db_create_user("Tester", "testuser", "tester@example.com", "password", conn=file)
        dbc.db_create_habit_data(1, "Tester", "testhabit1", "this is a test", False, False, conn=file)
        dbc.db_create_habit_data(1, "Tester", "testhabit2", "this is also a test", False, False, conn=file)
        dbc.db_create_habit_sub(1, 1, "2000-1-1", None, "Daily", 0, 0, conn=file)
        dbc.db_create_habit_sub(1, 2, "2000-1-2", None, "Daily", 0, 0, conn=file)

    def test_get_user_display_name(self) -> None:
        result = request.get_user_displayname(1, conn=file)
        self.assertEqual(result, "Tester")

    def test_get_user_subs_success(self) -> None:
        result = request.get_subs_for_user(1, conn=file)
        self.assertEqual(len(result), 2)

    def test_create_completions(self) -> None:
        r1 = request.create_completion(sub.Completion(user_id=1, habit_sub_id=1, compl_date=date.today()), conn=file)
        r2 = request.create_completion(sub.Completion(user_id=1, habit_sub_id=1, compl_date=date.today() - timedelta(days=1)), conn=file)
        r3 = request.create_completion(sub.Completion(user_id=1, habit_sub_id=2, compl_date=date.today() - timedelta(days=3)), conn=file)
        self.assertTrue(r1==r2==r3==True)

    def test_get_users_sub_completions(self) -> None:
        r1 = request.get_all_sub_completions_for_user(user_id=1, sub_id=1, conn=file)
        r2 = request.get_all_sub_completions_for_user(user_id=1, sub_id=2, conn=file)
        self.assertTrue(len(r1) == 2 and len(r2) == 1)

    @classmethod
    def tearDownClass(cls):
        os.remove(file.value) if os.path.exists(file.value) else None

#* ********************************************* HabitData *********************************************

class TestHabitDataRequests(unittest.TestCase):
    """"""
    @classmethod
    def setUpClass(cls) -> None:
        os.remove(file.value) if os.path.exists(file.value) else None
        dbc.db_init(file)

        # Setup pre-reqs (these are tested in db_test.py)
        dbc.db_create_user("Tester", "testuser", "tester@example.com", "password", conn=file)

    def test_create_and_get_habit_data(self) -> None:
        test_data = data.HabitData(
            habit_id=999,
            name="VeryUniqueNameToIdThisHabit",
            desc="TestDesc",
            author_id=1,
            author_name="Tester"
        )
        habit_id = request.create_new_habit_via_obj(test_data, conn=file)
        result:data.HabitData|None = request.get_habit_data(habit_id, conn=file)
        if result:
            self.assertEqual(result.name, "VeryUniqueNameToIdThisHabit")
        else:
            self.assertTrue(False)

    def test_edit_habit_data(self) -> None:
        pass

    def test_delete_habit_data(self) -> None:
        test_data = data.HabitData(
            habit_id=998,
            name="TestName",
            desc="TestDesc",
            author_id=1,
            author_name="Tester"
        )
        habit_id = request.create_new_habit_via_obj(test_data, conn=file)
        result = request.delete_habit_data(habit_id, conn=file)

        self.assertTrue(result and not dbc.db_get_habit_data_by_id(habit_id, conn=file))

    @classmethod
    def tearDownClass(cls):
        os.remove(file.value) if os.path.exists(file.value) else None
