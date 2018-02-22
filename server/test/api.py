import json
from tornado.testing import AsyncTestCase, AsyncHTTPTestCase

from storage.riak import RiakDb
import serve2

class ServerTest(AsyncHTTPTestCase):
    def setUp(self):
        self.db = RiakDb()
        self.db.create_user("test", "test", "test")
        super().setUp()

    def tearDown(self):
        self.db.delete_user("test")
        super().tearDown()

    def get_app(self):
        return serve2.Application(self.db)

class TestLogin(ServerTest):
    def tearDown(self):
        self.db.delete_user("test2")
        super().tearDown()

    def test_login(self):
        response = self.fetch("/api/login", method="POST", body="email=test&password=test")
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["status"], "success")

    def test_failed_login(self):
        response = self.fetch("/api/login", method="POST", body="email=no&password=fake")
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["status"], "failure")

    def test_signup(self):
        response = self.fetch("/api/users", method="POST", body=json.dumps({"data":{"attributes":{"email":"test2","name":"test2","password":"test2"}}}))
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["status"], "success")
        response = self.fetch("/api/login", method="POST", body="email=test2&password=test2")
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["status"], "success")


class AuthenticatedServerTest(ServerTest):
    def setUp(self):
        super().setUp()
        response = self.fetch("/api/login", method="POST", body="email=test&password=test")
        self.cookie = response.headers["set-cookie"]

class TestPolygon(AuthenticatedServerTest):
    def setUp(self):
        super().setUp()
        self.db.create_polygon("991", "loc1", "name1", "test")
        self.db.create_polygon("992", "loc2", "name2", "other_user")

    def tearDown(self):
        self.db.delete_polygon("991")
        self.db.delete_polygon("992")
        super().tearDown()

    def test_get_own_polygon(self):
        response = self.fetch("/api/polygons/991", headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "name1")

    def test_cant_get_not_own_polygon(self):
        response = self.fetch("/api/polygons/992", headers=dict(cookie=self.cookie))
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["error"], "not found")

    def test_create_get_delete_polygon(self):
        response = self.fetch("/api/polygons", method="POST", headers=dict(cookie=self.cookie), body=json.dumps({"data":{"id":993,"attributes":{"name":"created","location":"loc3"}}}))
        self.assertEqual(response.code, 200)

        response = self.fetch("/api/polygons/993", headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "created")

        response = self.fetch("/api/polygons/993", method="DELETE", headers=dict(cookie=self.cookie))
        self.assertEqual(response.code, 200)
