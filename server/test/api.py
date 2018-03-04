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
        self.assertEqual(data["error"], "user already exists")


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
        print(response)
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

    def test_cant_get_other_user(self):
        response = self.fetch("/api/users/" + self.id_u1,
                              headers=dict(cookie=self.cookie))
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["error"], "not found")

    def test_cant_delete_other_user(self):
        response = self.fetch("/api/users/" + self.id_u1, method="DELETE",
                              headers=dict(cookie=self.cookie))
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["error"], "not found")


class TestPolygons(AuthenticatedServerTest):
    def setUp(self):
        super().setUp()
        p1 = self.db.create_polygon("loc1", "name1", TEST_EMAIL)
        p2 = self.db.create_polygon("loc2", "name2", "other_user")
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
            "attributes": {"name": "updated_name"}
        }})
        response = self.fetch("/api/polygons/" + self.id_p1, method="PATCH",
                              headers=dict(cookie=self.cookie), body=body)
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "updated_name")

        response = self.fetch("/api/polygons/" + self.id_p1,
                              headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "updated_name")
        self.assertEqual(resp["data"]["attributes"]["location"], "loc1")

    def test_cant_get_not_own_polygon(self):
        response = self.fetch("/api/polygons/" + self.id_p2,
                              headers=dict(cookie=self.cookie))
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["error"], "not found")

    def test_create_get_delete_polygon(self):
        body = json.dumps({"data": {"attributes": {
            "name": "created",
            "location": "loc3"
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

        response = self.fetch("/api/polygons/" + poly_id, method="DELETE",
                              headers=dict(cookie=self.cookie))
        self.assertEqual(response.code, 200)

    def test_cant_delete_not_own_polygon(self):
        response = self.fetch("/api/polygons/" + self.id_p2, method="DELETE",
                              headers=dict(cookie=self.cookie))
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["error"], "not found")
