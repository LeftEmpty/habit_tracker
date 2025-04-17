import unittest
import sqlite3
import sys, os 
sys.path.append(os.path.abspath("."))

import db.src.controller as con

file = con.Connection.TEST

class TestUserValidCreation(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        con.db_init_db(file)

    def test_create_user_valid(self):
        user_id = con.db_create_user("testuser", "user1", "test@example.com", "passowrd", file)
        self.assertNotEqual(user_id, False)

    @classmethod
    def tearDownClass(cls):
        #delete the test database after tests are done
        os.remove("test.sqlite")

class TestUserInvalidCreation(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        con.db_init_db(file)

    def test_create_user_duplicate(self):
        con.db_create_user("testuser", "user1", "test@example.com", "passowrd", file)
        user_id= con.db_create_user("testuser", "user1", "test@example.com", "passowrd", file)
        self.assertEqual(user_id, False)

    @classmethod
    def tearDownClass(cls):
        #delete the test database after tests are done
        os.remove("test.sqlite")


class TestGetUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        con.db_init_db(file)

    def test_get_user_by_id(self):
        user= con.db_create_user("testuser", "user1", "test@example.com", "passowrd", file)
        self.assertEqual(1, con.db_get_user_by_id(1, file)[0][0])

    @classmethod
    def tearDownClass(cls):
        #delete the test database after tests are done
        os.remove("test.sqlite")

class TestGetUserNotFound(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        con.db_init_db(file)

    def test_get_user_by_id_wrong(self):
        user= con.db_create_user("testuser", "user1", "test@example.com", "passowrd", file)
        self.assertEqual([], con.db_get_user_by_id(2, file))

    @classmethod
    def tearDownClass(cls):
        #delete the test database after tests are done
        os.remove("test.sqlite")


class TestDeleteUser(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        con.db_init_db(file)
    def test_delete_user(self):
        user= con.db_create_user("testuser", "user1", "test@example.com", "passowrd", file)
        con.db_delete_user(1, file)
        self.assertEqual(0, len(con.db_get_user_by_id(1, file)))


class TestCreateHabit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        con.db_init_db(file)

    def test_create_habit(self):
        con.db_create_user("testuser", "user1", "test@example.com", "passowrd", file)
        habit = con.db_create_habit(1, "testhabit", "this is a test habit", True, file)
        self.assertEqual(1, len(con.db_get_habit_by_id(1, file)))

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None


class TestGetUserByCredentials(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        con.db_init_db(file)

    def test_get_user_by_credentials(self):
        con.db_create_user("testuser", "user1", "test@example.com", "passowrd", file)
        user = con.db_get_userid_by_credentials("user1", "passowrd", file)
        self.assertEqual(1, user)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None


class TestGetUserByCredentialsFail(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        con.db_init_db(file)

    def test_get_user_by_credentials_fail(self):
        con.db_create_user("testuser", "user1", "test@example.com", "passowrd", file)
        user = con.db_get_userid_by_credentials("nonexistentuser", "wrongpassword", file)
        self.assertEqual(-1, user)


class TestDeleteUserFail(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        con.db_init_db(file)

    def test_delete_user_fail(self):
        con.db_create_user("testuser", "user1", "test@example.com", "password", file)
        result = con.db_delete_user(999, file)
        self.assertFalse(result)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None


class TestDeleteHabitFail(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        con.db_init_db(file)
    
    def test_delete_habit_fail(self):
        con.db_create_user("testuser", "user1", "test@example.com", "password", file)
        con.db_create_habit(1, "testhabit", conn=file)
        result = con.db_delete_habit(999, file)
        self.assertFalse(result)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None


class TestDeleteHabit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        con.db_init_db(file)

    def test_delete_habit_success(self):
        con.db_create_user("testuser", "user1", "test@example.com", "password", file)
        con.db_create_habit(1, "testhabit", conn=file)
        result = con.db_delete_habit(1, file)
        self.assertTrue(result)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None


if __name__ == '__main__':
    unittest.main()
