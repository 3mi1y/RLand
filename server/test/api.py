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
    def test_login(self):
        response = self.fetch("/login", method="POST", body="email=test&password=test")
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["status"], "success")

    def test_failed_login(self):
        response = self.fetch("/login", method="POST", body="email=no&password=fake")
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["status"], "failure")

class AuthenticatedServerTest(ServerTest):
    def setUp(self):
        super().setUp()
        response = self.fetch("/login", method="POST", body="email=test&password=test")
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
        response = self.fetch("/polygons/991", headers=dict(cookie=self.cookie))
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["name"], "name1")

    def test_cant_get_not_own_polygon(self):
        response = self.fetch("/polygons/992", headers=dict(cookie=self.cookie))
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["error"], "not found")
