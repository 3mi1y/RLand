import unittest

from storage.riak import RiakDb
from datetime import date

U_EMAIL = "test@example.com"
U_NAME = "Test User"
U_PASS = "test password"
U_ADDR = "test address"


class TestDbUsers(unittest.TestCase):
    def setUp(self):
        self.db = RiakDb()
        self.db.create_user(U_EMAIL, U_NAME, U_PASS, U_ADDR)

    def tearDown(self):
        self.db.delete_user(U_EMAIL)

    def test_get_user(self):
        self.assertEqual(self.db.get_user(U_EMAIL)['name'], U_NAME)

    def test_check_correct_password(self):
        self.assertTrue(self.db.login(U_EMAIL, U_PASS))

    def test_check_incorrect_password(self):
        self.assertFalse(self.db.login(U_EMAIL, "bad"))

    def test_delete_user(self):
        self.db.delete_user(U_EMAIL)
        self.assertIsNone(self.db.get_user(U_EMAIL))


class TestDbPolygons(unittest.TestCase):
    def setUp(self):
        self.db = RiakDb()
        self.db.create_user(U_EMAIL, U_NAME, U_PASS, U_ADDR)
        p = self.db.create_polygon("Nevada", "Area 51", U_EMAIL, date.today(), None, ['type1', 'typeB'])
        self.poly_id = p['id']

    def tearDown(self):
        self.db.delete_polygon(self.poly_id)
        self.db.delete_user(U_EMAIL)

    def test_get_own_polygon(self):
        poly = self.db.get_polygon(self.poly_id, U_EMAIL)
        self.assertEqual(poly['name'], "Area 51")
        self.assertEqual(poly['type'], ['type1', 'typeB'])

    def test_polygon_start_date_as_datetime(self):
        dt = self.db.get_polygon(self.poly_id, U_EMAIL)['start_date']
        self.assertEqual(dt, date.today())

    def test_get_other_polygon(self):
        self.assertIsNone(self.db.get_polygon(self.poly_id, "wrong_user"))

    def test_delete_polygon(self):
        self.db.delete_polygon(self.poly_id)
        self.assertIsNone(self.db.get_polygon(self.poly_id, U_EMAIL))


class TestDbPolygonTypes(unittest.TestCase):
    def setUp(self):
        self.db = RiakDb()
        self.db.create_poly_type("Test", False, None, ["child1", "child2"])

    def tearDown(self):
        self.db.delete_polygon("Test")
        self.db.delete_user(U_EMAIL)

    def test_get_poly_type(self):
        self.assertEqual(self.db.get_poly_type("Test")['children'][0],
                         "child1")

    # TODO: test_get_deleted_poly_type

    def test_delete_poly_type(self):
        self.db.delete_poly_type("Test")
        self.assertIsNone(self.db.get_poly_type("Test"))


class TestDbPolygonTasks(unittest.TestCase):
    def setUp(self):
        self.db = RiakDb()
        task = self.db.create_task(1, "water tomatoes", str(date.today()), 1, False, "water the tomatoes")
        self.task_id = task['id']

    def tearDown(self):
        self.db.delete_user(U_EMAIL)
        self.db.delete_task(self.task_id)

    def test_get_own_task(self):
        name = self.db.get_task(self.task_id)['name']
        self.assertEqual(name, "water tomatoes")

    def test_delete_task(self):
        self.db.delete_task(self.task_id)
        self.assertIsNone(self.db.get_task(self.task_id))


class TestDbPolygonNotes(unittest.TestCase):
    def setUp(self):
        self.db = RiakDb()
        note = self.db.create_note(1, str(date.today()), "NoteTitle", "NoteContent")
        self.note_id = note['id']

    def tearDown(self):
        self.db.delete_note(self.note_id)
        self.db.delete_user(U_EMAIL)

    def test_get_note(self):
        title = self.db.get_note(self.note_id)['title']
        self.assertEqual(title, "NoteTitle")

    def test_delete_note(self):
        self.db.delete_note(self.note_id)
        self.assertIsNone(self.db.get_note(self.note_id))


class TestDbPolygonHarvest(unittest.TestCase):
    def setUp(self):
        self.db = RiakDb()
        harvest = self.db.create_harvest(1, str(date.today()), 5, "bushels")
        self.harvest_id = harvest['id']

    def tearDown(self):
        self.db.delete_harvest(self.harvest_id)
        self.db.delete_user(U_EMAIL)

    def test_get_own_harvest(self):
        units = self.db.get_harvest(self.harvest_id)['units']
        self.assertEqual(units, "bushels")

    def test_delete_task(self):
        self.db.delete_harvest(self.harvest_id)
        self.assertIsNone(self.db.get_harvest(self.harvest_id))
