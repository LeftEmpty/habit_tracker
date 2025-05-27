import unittest
import sys, os
sys.path.append(os.path.abspath("."))

import db.controller as dbc


file = dbc.Connection.TEST


#* ********************************************* User *********************************************
class TestUserCreation(unittest.TestCase):
    """"""
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        dbc.db_init(file)

    def test_create_user_valid(self):
        result = dbc.db_create_user("testuser", "very_unique_name", "unique_email@test.com", "password", conn=file)
        self.assertEqual(result, True)

    def test_create_user_duplicate_username(self):
        dbc.db_create_user("testuser", "duplicate_name", "test1@example.com", "password", conn=file)
        result = dbc.db_create_user("testuser", "duplicate_name", "test2@example.com", "password", conn=file)
        self.assertNotEqual(result, True)

    def test_create_user_duplicate_email(self):
        dbc.db_create_user("testuser", "user1", "duplicate@example.com", "password", conn=file)
        result = dbc.db_create_user("testuser", "user2", "duplicate@example.com", "password", conn=file)
        self.assertNotEqual(result, True)

    @classmethod
    def tearDownClass(cls):
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None


class TestUserGetter(unittest.TestCase):
    """"""
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        dbc.db_init(file)

    def test_get_user_by_id_success(self):
        user= dbc.db_create_user("testuser", "user1", "test@example.com", "password", file)
        self.assertEqual(1, dbc.db_get_user_by_id(1, file)[0][0])

    def test_get_user_by_id_fail(self):
        user= dbc.db_create_user("testuser", "user1", "test@example.com", "password", file)
        self.assertEqual([], dbc.db_get_user_by_id(999, file))

    def test_get_user_by_credentials_found(self):
        dbc.db_create_user("testuser", "user1", "test@example.com", "password", file)
        user = dbc.db_get_userid_by_credentials("user1", "password", file)
        self.assertEqual(1, user)

    def test_get_user_by_credentials_notfound(self):
        dbc.db_create_user("testuser", "user1", "test@example.com", "password", file)
        user = dbc.db_get_userid_by_credentials("nonexistentuser", "wrongpassword", file)
        self.assertEqual(-1, user)

    @classmethod
    def tearDownClass(cls):
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None


class TestUserDeletion(unittest.TestCase):
    """"""
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        dbc.db_init(file)

    def test_delete_user_success(self):
        user= dbc.db_create_user("testuser", "user1", "test@example.com", "password", file)
        dbc.db_delete_user(user_id=1, conn=file)
        self.assertEqual(0, len(dbc.db_get_user_by_id(1, file)))

    def test_delete_user_fail_invalid_id(self):
        dbc.db_create_user("testuser", "user1", "test@example.com", "password", file)
        result = dbc.db_delete_user(user_id=999, conn=file)
        self.assertFalse(result)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None


#* ********************************************* HabitData *********************************************
class TestHabitDataCreation(unittest.TestCase):
    """"""
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        dbc.db_init(file)

    def test_create_habit_success(self):
        dbc.db_create_user("testuser", "user1", "test@example.com", "password", file)
        habit = dbc.db_create_habit_data(1, "test_author", "testhabit", "this is a test habit", False, False, conn=file)
        self.assertEqual(1, len(dbc.db_get_habit_data_by_id(1, file)))

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None


class TestHabitDataDeletion(unittest.TestCase):
    """"""
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        dbc.db_init(file)

        dbc.db_create_user("testuser", "user1", "test@example.com", "password", file) # has id 1

    def test_delete_habit_data_success(self):
        data_id = dbc.db_create_habit_data(1, "test_author", "testhabit", "test desc", False, False, conn=file)
        result = dbc.db_delete_habit_data(data_id, file)
        self.assertTrue(result)

    def test_delete_habit_data_fail(self):
        data_id = dbc.db_create_habit_data(1, "test_author", "testhabit", "this is a test habit", False, False, conn=file)
        result = dbc.db_delete_habit_data(data_id+1, conn=file)
        self.assertFalse(result)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None

#* ********************************************* HabitSubscription *********************************************
class TestHabitSubCreation(unittest.TestCase):
    """"""
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        dbc.db_init(file)

        dbc.db_create_user("testuser", "user1", "test@example.com", "password", file)

    def test_create_sub_success(self):
        data_id = dbc.db_create_habit_data(1, "test_author", "testhabit", "this is a test habit", False, False, conn=file)
        result = dbc.db_create_habit_sub(1, data_id, "2000-20-02", None, "Daily", 1, 1, conn=file)
        self.assertNotEqual(-1, result)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None


class TestHabitSubDeletion(unittest.TestCase):
    """"""
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        dbc.db_init(file)

        dbc.db_create_user("testuser", "user1", "test@example.com", "password", file) # has id 1

    def test_delete_habit_sub_success(self):
        data_id = dbc.db_create_habit_data(1, "test_author", "testhabit", "this is a test habit", False, False, conn=file)
        sub_id = dbc.db_create_habit_sub(1, data_id, "2000-20-02", None, "Daily", 1, 1, file)
        result = dbc.db_delete_habit_sub(sub_id, conn=file)
        self.assertTrue(result)

    def test_delete_habit_sub_fail(self):
        data_id = dbc.db_create_habit_data(1, "test_author", "testhabit", "this is a test habit", False, False, conn=file)
        sub_id = dbc.db_create_habit_sub(1, data_id, "2000-20-02", None, "Daily", 1, 1, file)
        result = dbc.db_delete_habit_sub(sub_id+1, conn=file)
        self.assertFalse(result)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None


#* ********************************************* Completion *********************************************
class TestCompletionCreation(unittest.TestCase):
    """"""
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        dbc.db_create_user("testuser", "user1", "test@example.com", "password", file)
        dbc.db_init(file)

    def test_create_sub_success(self):
        data_id = dbc.db_create_habit_data(1, "test_author", "testhabit", "this is a test habit", False, False, conn=file)
        result = dbc.db_create_habit_sub(1, data_id, "2000-20-02", None, "Daily", 1, 1, file)
        self.assertNotEqual(-1, result)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None


if __name__ == '__main__':
    unittest.main()
