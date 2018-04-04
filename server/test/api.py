from datetime import date
import json
from tornado.testing import AsyncHTTPTestCase

from storage.riak import RiakDb
import serve2

TEST_EMAIL = "test@example.com"


class ServerTest(AsyncHTTPTestCase):
    def setUp(self):
        self.db = RiakDb()
        self.db.create_user(TEST_EMAIL, "test name", "testpass", "New York")
        super().setUp()

    def tearDown(self):
        self.db.delete_user(TEST_EMAIL)
        super().tearDown()

    def get_app(self):
        return serve2.Application(self.db)


class TestLogin(ServerTest):
    def tearDown(self):
        self.db.delete_user("test2")
        super().tearDown()

    def test_login(self):
        response = self.fetch("/api/login", method="POST",
                              body="email=test@example.com&password=testpass")
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["status"], "success")

    def test_failed_login(self):
        response = self.fetch("/api/login", method="POST",
                              body="email=no&password=fake")
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["status"], "failure")

    def test_signup_login(self):
        body = json.dumps({"data": {
            "attributes": {
                "email": "test2",
                "name": "test2",
                "password": "test2",
                "address": "address2"
            }
        }})
        response = self.fetch("/api/users", method="POST", body=body)
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["data"]["attributes"]["name"], "test2")
        response = self.fetch("/api/login", method="POST",
                              body="email=test2&password=test2")
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["status"], "success")

    def test_cant_signup_duplicate(self):
        body = json.dumps({"data": {
            "attributes": {
                "email": "test2",
                "name": "test2",
                "password": "test2",
                "address": "address2"
            }
        }})
        response = self.fetch("/api/users", method="POST", body=body)
        data = json.loads(str(response.body, "utf-8"))

        response = self.fetch("/api/users", method="POST", body=body)
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["errors"][0]["title"], "user already exists")


class AuthenticatedServerTest(ServerTest):
    def setUp(self):
        super().setUp()
        response = self.fetch("/api/login", method="POST",
                              body="email=test@example.com&password=testpass")
        self.cookie = response.headers["set-cookie"]


class TestUsers(AuthenticatedServerTest):
    def setUp(self):
        super().setUp()
        self.id_me = "test@example.com"
        self.db.create_user("other@example.com", "user 2", "testpass",
                            "New York")
        self.id_u1 = "other@example.com"

    def tearDown(self):
        self.db.delete_user(self.id_u1)
        super().tearDown()

    def test_get_own_user(self):
        response = self.fetch("/api/users/" + self.id_me,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "test name")

    def test_update_own_user(self):
        body = json.dumps({"data": {
            "id": self.id_me,
            "attributes": {"address": "Paris"}
        }})
        response = self.fetch("/api/users/" + self.id_me, method="PATCH",
                              headers=dict(cookie=self.cookie), body=body)
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["address"], "Paris")

        response = self.fetch("/api/users/" + self.id_me,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "test name")
        self.assertEqual(resp["data"]["attributes"]["address"], "Paris")

    def test_change_password(self):
        body = json.dumps({"data": {
            "attributes": {"password": "newpass", "old-password": "testpass"}
        }})
        response = self.fetch("/api/users/" + self.id_me, method="PATCH",
                              headers=dict(cookie=self.cookie), body=body)
        self.assertEqual(response.code, 200)

        response = self.fetch("/api/login", method="POST",
                              body="email=test@example.com&password=testpass")
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["status"], "failure")

        response = self.fetch("/api/login", method="POST",
                              body="email=test@example.com&password=newpass")
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["status"], "success")

    def test_cant_update_email_address(self):
        body = json.dumps({"data": {
            "id": self.id_me,
            "attributes": {"email": "evil.com", "address": "Paris"}
        }})
        response = self.fetch("/api/users/" + self.id_me, method="PATCH",
                              headers=dict(cookie=self.cookie), body=body)
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["errors"][0]["title"], "cannot change user email address")

    def test_cant_get_other_user(self):
        response = self.fetch("/api/users/" + self.id_u1,
                              headers=dict(cookie=self.cookie))
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["errors"][0]["title"], "not found")

    def test_cant_delete_other_user(self):
        response = self.fetch("/api/users/" + self.id_u1, method="DELETE",
                              headers=dict(cookie=self.cookie))
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["errors"][0]["title"], "not found")


class TestPolygons(AuthenticatedServerTest):
    def setUp(self):
        super().setUp()
        p1 = self.db.create_polygon("loc1", "name1", TEST_EMAIL, date.today(), None, ["Plant", "Vegetable"])
        p2 = self.db.create_polygon("loc2", "name2", "other_user", date.today(), None, ["Structure", "Barn"])
        self.id_p1 = p1["id"]
        self.id_p2 = p2["id"]

    def tearDown(self):
        self.db.delete_polygon(self.id_p1)
        self.db.delete_polygon(self.id_p2)
        super().tearDown()

    def test_get_own_polygon(self):
        response = self.fetch("/api/polygons/" + self.id_p1,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "name1")

    def test_update_own_polygon(self):
        body = json.dumps({"data": {
            "id": self.id_p1,
            "attributes": {"name": "updated_name", "end-date": "2017-03-05"}
        }})
        response = self.fetch("/api/polygons/" + self.id_p1, method="PATCH",
                              headers=dict(cookie=self.cookie), body=body)
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "updated_name")
        self.assertEqual(resp["data"]["attributes"]["end-date"], "2017-03-05")

        response = self.fetch("/api/polygons/" + self.id_p1,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "updated_name")
        self.assertEqual(resp["data"]["attributes"]["location"], "loc1")

    def test_cant_get_not_own_polygon(self):
        response = self.fetch("/api/polygons/" + self.id_p2,
                              headers=dict(cookie=self.cookie))
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["errors"][0]["title"], "not found")

    def test_create_get_delete_polygon(self):
        body = json.dumps({"data": {"attributes": {
            "name": "created",
            "location": "loc3",
            "start-date": str(date.today()),
            "end-date": None,
            "poly-type": ["Animal", "Chicken"],
        }}})
        response = self.fetch("/api/polygons", method="POST",
                              headers=dict(cookie=self.cookie), body=body)
        self.assertEqual(response.code, 200)
        resp = json.loads(str(response.body, "utf-8"))
        poly_id = resp['data']['id']

        response = self.fetch("/api/polygons/" + poly_id,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "created")
        self.assertEqual(resp["data"]["attributes"]["end-date"], None)
        self.assertEqual(resp["data"]["attributes"]["poly-type"], ["Animal", "Chicken"])

        response = self.fetch("/api/polygons/" + poly_id, method="DELETE",
                              headers=dict(cookie=self.cookie))
        self.assertEqual(response.code, 204)

    def test_cant_delete_not_own_polygon(self):
        response = self.fetch("/api/polygons/" + self.id_p2, method="DELETE",
                              headers=dict(cookie=self.cookie))
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["errors"][0]["title"], "not found")


class TestNotes(AuthenticatedServerTest):
    def setUp(self):
        super().setUp()
        poly = self.db.create_polygon("location", "name", TEST_EMAIL, date.today(), None, [])
        self.id_poly = poly["id"]

        user = self.db.get_user(TEST_EMAIL)
        user['polygon_ids'] += [self.id_poly]
        self.db.update_user(user)

        note = self.db.create_note(self.id_poly, "2018-07-12", "test", "test content")
        self.id_note = note["id"]

    def tearDown(self):
        self.db.delete_note(self.id_note)
        self.db.delete_polygon(self.id_poly)
        super().tearDown()

    def test_get_note(self):
        response = self.fetch("/api/notes/" + self.id_note,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["title"], "test")

    def test_update_note(self):
        body = json.dumps({"data": {
            "id": self.id_note,
            "attributes": {"date": "2017-05-12"}
        }})
        response = self.fetch("/api/notes/" + self.id_note, method="PATCH",
                              headers=dict(cookie=self.cookie), body=body)
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["title"], "test")
        self.assertEqual(resp["data"]["attributes"]["date"], "2017-05-12")

        response = self.fetch("/api/notes/" + self.id_note,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["date"], "2017-05-12")
        self.assertEqual(resp["data"]["attributes"]["title"], "test")

    def test_create_get_delete_note(self):
        body = json.dumps({"data": {"attributes": {
            "poly-id": self.id_poly,
            "date": None,
            "title": "new note",
            "content": "hello world",
        }}})
        response = self.fetch("/api/notes", method="POST",
                              headers=dict(cookie=self.cookie), body=body)
        self.assertEqual(response.code, 200)
        resp = json.loads(str(response.body, "utf-8"))
        note_id = resp['data']['id']

        response = self.fetch("/api/notes/" + note_id,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["poly-id"], self.id_poly)
        self.assertEqual(resp["data"]["attributes"]["date"], None)
        self.assertEqual(resp["data"]["attributes"]["title"], "new note")

        response = self.fetch("/api/notes/" + note_id, method="DELETE",
                              headers=dict(cookie=self.cookie))
        self.assertEqual(response.code, 204)


class TestHarvests(AuthenticatedServerTest):
    def setUp(self):
        super().setUp()
        poly = self.db.create_polygon("location", "name", TEST_EMAIL, date.today(), None, [])
        self.id_poly = poly["id"]

        user = self.db.get_user(TEST_EMAIL)
        user['polygon_ids'] += [self.id_poly]
        self.db.update_user(user)

        harvest = self.db.create_harvest(self.id_poly, "2018-01-13", 3, "lbs")
        self.id_harvest = harvest["id"]

    def tearDown(self):
        self.db.delete_harvest(self.id_harvest)
        self.db.delete_polygon(self.id_poly)
        super().tearDown()

    def test_get_harvest(self):
        response = self.fetch("/api/harvests/" + self.id_harvest,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["amount"], 3)

    def test_update_harvest(self):
        body = json.dumps({"data": {
            "id": self.id_harvest,
            "attributes": {"date": "2017-04-14", "units": "count"}
        }})
        response = self.fetch("/api/harvests/" + self.id_harvest, method="PATCH",
                              headers=dict(cookie=self.cookie), body=body)
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["date"], "2017-04-14")
        self.assertEqual(resp["data"]["attributes"]["units"], "count")

        response = self.fetch("/api/harvests/" + self.id_harvest,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["date"], "2017-04-14")
        self.assertEqual(resp["data"]["attributes"]["amount"], 3)

    def test_create_get_delete_harvest(self):
        body = json.dumps({"data": {"attributes": {
            "poly-id": self.id_poly,
            "date": None,
            "amount": 3,
            "units": "bushels",
        }}})
        response = self.fetch("/api/harvests", method="POST",
                              headers=dict(cookie=self.cookie), body=body)
        self.assertEqual(response.code, 200)
        resp = json.loads(str(response.body, "utf-8"))
        harvest_id = resp['data']['id']

        response = self.fetch("/api/harvests/" + harvest_id,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["poly-id"], self.id_poly)
        self.assertEqual(resp["data"]["attributes"]["units"], "bushels")

        response = self.fetch("/api/harvests/" + harvest_id, method="DELETE",
                              headers=dict(cookie=self.cookie))
        self.assertEqual(response.code, 204)


class TestTasks(AuthenticatedServerTest):
    def setUp(self):
        super().setUp()
        poly = self.db.create_polygon("location", "name", TEST_EMAIL, date.today(), None, [])
        self.id_poly = poly["id"]

        user = self.db.get_user(TEST_EMAIL)
        user['polygon_ids'] += [self.id_poly]
        self.db.update_user(user)

        task = self.db.create_task(self.id_poly, "do task", "2018-08-11")
        self.id_task = task["id"]

    def tearDown(self):
        self.db.delete_task(self.id_task)
        self.db.delete_polygon(self.id_poly)
        super().tearDown()

    def test_get_task(self):
        response = self.fetch("/api/tasks/" + self.id_task,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "do task")

    def test_update_task(self):
        body = json.dumps({"data": {
            "id": self.id_task,
            "attributes": {"name": "new name"}
        }})
        response = self.fetch("/api/tasks/" + self.id_task, method="PATCH",
                              headers=dict(cookie=self.cookie), body=body)
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "new name")
        self.assertEqual(resp["data"]["attributes"]["due-date"], "2018-08-11")

        response = self.fetch("/api/tasks/" + self.id_task,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "new name")
        self.assertEqual(resp["data"]["attributes"]["due-date"], "2018-08-11")

    def test_create_get_delete_task(self):
        body = json.dumps({"data": {"attributes": {
            "poly-id": self.id_poly,
            "due-date": None,
            "name": "hello world",
        }}})
        response = self.fetch("/api/tasks", method="POST",
                              headers=dict(cookie=self.cookie), body=body)
        self.assertEqual(response.code, 200)
        resp = json.loads(str(response.body, "utf-8"))
        task_id = resp['data']['id']

        response = self.fetch("/api/tasks/" + task_id,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["poly-id"], self.id_poly)
        self.assertEqual(resp["data"]["attributes"]["name"], "hello world")

        response = self.fetch("/api/tasks/" + task_id, method="DELETE",
                              headers=dict(cookie=self.cookie))
        self.assertEqual(response.code, 204)


class TestPolygonTypes(AuthenticatedServerTest):
    def setUp(self):
        super().setUp()
        self.db.create_poly_type("Test Plant", False, None, ["Test Vegetable Garden"])
        self.db.create_poly_type("Test Vegetable Garden", True, "crop", ["Test Tomato"])

    def tearDown(self):
        self.db.delete_poly_type("Test Plant")
        self.db.delete_poly_type("Test Vegetable Garden")
        super().tearDown()

    def test_get_poly_type(self):
        response = self.fetch("/api/polygon_types/Test%20Plant", headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["children"][0], "Test Vegetable Garden")

    def test_update_poly_type(self):
        response = self.fetch("/api/polygon_types/Test%20Plant", method="PATCH", headers=dict(cookie=self.cookie),
                              body=json.dumps({"data": {"attributes": {"children": ["Test Tomato", "Test Potato"]}}}))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["children"][1], "Test Potato")

        response = self.fetch("/api/polygon_types/Test%20Plant", headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["id"], "Test Plant")
        self.assertEqual(resp["data"]["attributes"]["children"][0], "Test Tomato")

    def test_create_get_delete_poly_type(self):
        response = self.fetch("/api/polygon_types", method="POST", headers=dict(cookie=self.cookie),
                              body=json.dumps({"data": {"id": "Test Type", "attributes": {
                                "is_container": False,
                                "harvest": None,
                                "children": []
                              }}}))
        self.assertEqual(response.code, 200)
        resp = json.loads(str(response.body, "utf-8"))

        response = self.fetch("/api/polygon_types/Test%20Type", headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["children"], [])

        response = self.fetch("/api/polygon_types/Test%20Type", method="DELETE", headers=dict(cookie=self.cookie))
        self.assertEqual(response.code, 204)
