from tornado.testing import AsyncTestCase, AsyncHTTPTestCase

from storage.riak import RiakDb
import serve2

class TestLogin(AsyncHTTPTestCase):
    def get_app(self):
        db = RiakDb()
        return serve2.Application(db)

    # TODO: make these tests make sense
    def test_login(self):
        response = self.fetch("/login", method="POST", body="email=test&password=test")
        self.assertEqual(response.code, 200)

    def test_failed_login(self):
        response = self.fetch("/login", method="POST", body="email=no&password=fake")
        self.assertNotEqual(response.code, 200)
