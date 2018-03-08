import unittest

from storage.riak import RiakDb
import storage.security as security
from datetime import datetime, date

U_EMAIL = "test@example.com"
U_NAME = "Test User"
U_PASS = "test password"
U_ADDR = "test address"


class TestDbUsers(unittest.TestCase):
    def setUp(self):
        self.db = RiakDb()
        self.db.create_user(U_EMAIL, U_NAME, U_PASS, U_ADDR)

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


class TestDbPolygons(unittest.TestCase):
    def setUp(self):
        self.db = RiakDb()
        self.db.create_user(U_EMAIL, U_NAME, U_PASS, U_ADDR)
        p = self.db.create_polygon("Nevada", "Area 51", U_EMAIL, date.today(), ['type1'])
        self.poly_id = p['id']

    def test_get_own_polygon(self):
        name = self.db.get_polygon(self.poly_id, U_EMAIL)['name']
        self.assertEqual(name, "Area 51")

    def test_polygon_start_date_as_datetime(self):
        dt = self.db.get_polygon(self.poly_id, U_EMAIL)['start_date']
        self.assertEqual(dt, date.today())

    def test_get_other_polygon(self):
        self.assertIsNone(self.db.get_polygon(self.poly_id, "wrong_user"))

    def test_delete_polygon(self):
        self.db.delete_polygon(self.poly_id)
        self.assertIsNone(self.db.get_polygon(self.poly_id, U_EMAIL))

    def tearDown(self):
        self.db.delete_polygon(self.poly_id)


class TestDbPolygonTypes(unittest.TestCase):
    def setUp(self):
        self.db = RiakDb()
        self.db.create_poly_type("Test", False, None, "test subtype")

    def test_get_poly_type(self):
        self.assertEqual(self.db.get_poly_type("Test")['subtype'],
                         "test subtype")

    # TODO: test_get_deleted_poly_type

    def test_delete_poly_type(self):
        self.db.delete_poly_type("Test")
        self.assertIsNone(self.db.get_poly_type("Test"))

    def tearDown(self):
        self.db.delete_polygon("Test")

class TestDbPolygonTasks:
    def setUp(self):
        self.db = RiakDb()
        task = self.db.create_task(1,"water tomatoes",datetime.date)
        self.task_id = task['id']
    def test_get_own_task(self):
        name = self.db.get_task(1,self.task_id)
        self.assertEqual(name,"water tomatoes")
    def test_get_other_task(self):
        self.assertIsNone(self.db.get_task(2,self.task_id))
    def test_delete_task(self):
        self.db.delete_polygon(self.task_id)
        self.assertIsNone(self.db.get_task(1,self.task_id))
    def tearDown(self):
        self.db.delete_task(self.task_id)
