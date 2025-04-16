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
        self.assertNotEqual(user_id, -1)
        self.assertNotEqual(user_id, -2)

    @classmethod
    def tearDownClass(cls):
        #delete the test database after tests are done
        os.remove("test.sqlite")

class TestUserInvalidCreation(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        os.remove("test.sqlite") if os.path.exists("test.sqlite") else None
        con.db_init_db(file)

    @unittest.expectedFailure
    def test_create_user_duplicate(self):
        con.db_create_user("testuser", "user1", "test@example.com", "passowrd", file)
        user_id= con.db_create_user("testuser", "user1", "test@example.com", "passowrd", file)
        self.assertNotEqual(user_id, -2)
        self.assertNotEqual(user_id, -1)

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

    @unittest.expectedFailure
    def test_get_user_by_id_wrong(self):
        user= con.db_create_user("testuser", "user1", "test@example.com", "passowrd", file)
        self.assertEqual(2, con.db_get_user_by_id(1, file)[0][0])

    @classmethod
    def tearDownClass(cls):
        #delete the test database after tests are done
        os.remove("test.sqlite")



if __name__ == '__main__':
    unittest.main()
