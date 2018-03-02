import unittest

from storage.riak import RiakDb
import storage.security as security

U_EMAIL = "test@example.com"
U_NAME = "Test User"
U_PASS = "test password"

class UserDbTests(unittest.TestCase):
    def setUp(self):
        self.db = RiakDb()
        self.db.create_user(U_EMAIL, U_NAME, U_PASS)

    def test_get_user(self):
        self.assertEqual(self.db.get_user(U_EMAIL)['name'], U_NAME) 

    def test_check_correct_password(self):
        pwhash = self.db.get_user(U_EMAIL)['password']
        self.assertTrue(security.check_password(U_PASS, pwhash))

    def test_check_incorrect_password(self):
        pwhash = self.db.get_user(U_EMAIL)['password']
        self.assertFalse(security.check_password("bad", pwhash))

    def test_delete_user(self):
        self.db.delete_user(U_EMAIL)
        self.assertIsNone(self.db.get_user(U_EMAIL))

    # TODO: test_get_deleted_user

class PolygonDbTests(unittest.TestCase):
    def setUp(self):
        self.db = RiakDb()
        self.db.create_user(U_EMAIL, U_NAME, U_PASS)
        p = self.db.create_polygon("Nevada", "Area 51", U_EMAIL)
        self.poly_id = p['id']

    def test_get_own_polygon(self):
        self.assertEqual(self.db.get_polygon(self.poly_id, U_EMAIL)['name'], "Area 51")

    def test_get_other_polygon(self):
        self.assertIsNone(self.db.get_polygon(self.poly_id, "wrong_user"))

    # TODO: test_get_deleted_polygon

    def test_delete_own_polygon(self):
        self.db.delete_polygon(self.poly_id)
        self.assertIsNone(self.db.get_polygon(self.poly_id, U_EMAIL))

    # TODO: test_delete_other_polygon?

    def tearDown(self):
        self.db.delete_polygon(self.poly_id)

class PolygonTypeDbTests(unittest.TestCase):
    def setUp(self):
        self.db = RiakDb()
        self.db.create_poly_type("Test", False, None, "test subtype")

    def test_get_poly_type(self):
        self.assertEqual(self.db.get_poly_type("Test")['subtype'], "test subtype")

    # TODO: test_get_deleted_poly_type

    def test_delete_poly_type(self):
        self.db.delete_poly_type("Test")
        self.assertIsNone(self.db.get_poly_type("Test"))

    def tearDown(self):
        self.db.delete_polygon("Test")
