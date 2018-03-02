import json
from tornado.testing import AsyncHTTPTestCase

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
        p1 = self.db.create_polygon("loc1", "name1", "test")
        p2 = self.db.create_polygon("loc2", "name2", "other_user")
        self.id_p1 = p1["id"]
        self.id_p2 = p2["id"]

    def tearDown(self):
        self.db.delete_polygon(self.id_p1)
        self.db.delete_polygon(self.id_p2)
        super().tearDown()

    def test_get_own_polygon(self):
        response = self.fetch("/api/polygons/" + self.id_p1, headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "name1")

    def test_update_own_polygon(self):
        response = self.fetch("/api/polygons/" + self.id_p1, method="PATCH", headers=dict(cookie=self.cookie),
            body=json.dumps({"data":{"id":self.id_p1, "attributes":{"name":"updated_name"}}})
            )
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "updated_name")

        response = self.fetch("/api/polygons/" + self.id_p1, headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "updated_name")
        self.assertEqual(resp["data"]["attributes"]["location"], "loc1")

    def test_cant_get_not_own_polygon(self):
        response = self.fetch("/api/polygons/" + self.id_p2, headers=dict(cookie=self.cookie))
        data = json.loads(str(response.body, "utf-8"))
        self.assertEqual(data["error"], "not found")

    def test_create_get_delete_polygon(self):
        response = self.fetch("/api/polygons", method="POST", headers=dict(cookie=self.cookie), body=json.dumps({"data":{"attributes":{"name":"created","location":"loc3"}}}))
        self.assertEqual(response.code, 200)
        resp = json.loads(str(response.body, "utf-8"))
        poly_id = resp['data']['id']

        response = self.fetch("/api/polygons/" + poly_id, headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["name"], "created")

        response = self.fetch("/api/polygons/" + poly_id, method="DELETE", headers=dict(cookie=self.cookie))
        self.assertEqual(response.code, 200)

class TestPolygonType(AuthenticatedServerTest):
    def setUp(self):
        super().setUp()
        self.db.create_poly_type("Plant", False, None, None)
        self.db.create_poly_type("Plant:Vegetable Garden", True, "crop", "Vegetable")

    def tearDown(self):
        self.db.delete_poly_type("Plant")
        self.db.delete_poly_type("Plant:Vegetable Garden")
        super().tearDown()

    def test_get_poly_type(self):
        response = self.fetch("/api/polygon_types/Plant", headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["subtype"], None)

    def test_update_poly_type(self):
        response = self.fetch("/api/polygon_types/Plant", method="PATCH", headers=dict(cookie=self.cookie),
            body=json.dumps({"data":{"attributes":{"subtype":"new_subtype"}}})
            )
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["subtype"], "new_subtype")

        response = self.fetch("/api/polygon_types/Plant", headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["id"], "Plant")
        self.assertEqual(resp["data"]["attributes"]["subtype"], "new_subtype")

    def test_create_get_delete_poly_type(self):
        response = self.fetch("/api/polygon_types", method="POST", headers=dict(cookie=self.cookie), body=json.dumps({"data":{"id":"Test Type","attributes":{"is_container":False,"harvest":None,"subtype":"st"}}}))
        self.assertEqual(response.code, 200)
        resp = json.loads(str(response.body, "utf-8"))

        response = self.fetch("/api/polygon_types/Test%20Type", headers=dict(cookie=self.cookie))
        resp = json.loads(str(response.body, "utf-8"))
        self.assertEqual(resp["data"]["attributes"]["subtype"], "st")

        response = self.fetch("/api/polygon_types/Test%20Type", method="DELETE", headers=dict(cookie=self.cookie))
        self.assertEqual(response.code, 200)
