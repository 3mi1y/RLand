import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.escape
import tornado.httpclient
import os.path
from tornado import gen


from tornado.options import define, options

from storage.riak import RiakDb

define("port", default=8000, help="run on the given port", type=int)


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        cookie_bytes = self.get_secure_cookie("userEmail")
        if not cookie_bytes:
            return None
        email = str(cookie_bytes, "utf-8")
        return self.settings['db'].get_user(email)

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


class MainHandler(BaseHandler):

    def get(self):
        f = open(os.path.join(os.path.dirname(__file__), "../ember-proj/dist/index.html"))
        index = f.read()
        self.write(index)


def jsonify_user(user):
    return {
        "type": "users",
        "id": user["email"],
        "attributes": {
            "name": user["name"],
            "address": user["address"],
            "polygon_ids": user["polygon_ids"],
        }
    }


class UsersHandler(BaseHandler):

    @gen.coroutine
    def post(self):
        bodyJSON = tornado.escape.json_decode(self.request.body)
        email = bodyJSON['data']['attributes']['email']
        name = bodyJSON['data']['attributes']['name']
        password = bodyJSON['data']['attributes']['password']
        address = bodyJSON['data']['attributes']['address']
        new_user = self.settings['db'].create_user(email, name, password, address)
        if new_user:
            self.write(dict(data=jsonify_user(new_user)))
        else:
            self.set_status(400)
            self.write(dict(errors=[{"title": "user already exists"}]))

    @tornado.web.authenticated
    def get(self, userEmail):
        if userEmail == "@CURRENT_USER":
            userEmail = self.current_user['email']

        if self.current_user['email'] != userEmail:
            self.set_status(404)
            self.write(dict(errors=[{"title": "not found"}]))
            return

        self.write({"data": jsonify_user(self.current_user)})

    @tornado.web.authenticated
    def patch(self, userEmail):
        db = self.settings['db']
        if self.current_user['email'] != userEmail:
            self.set_status(404)
            self.write(dict(errors=[{"title": "not found"}]))
            return

        user = self.current_user
        bodyJSON = tornado.escape.json_decode(self.request.body)
        attrs = bodyJSON['data']['attributes']

        if 'email' in attrs and attrs['email'] and attrs['email'] != userEmail:
            self.write(dict(errors=[{"title": "cannot change user email address"}]))
            return

        if 'password' in attrs and 'old-password' in attrs and attrs['password']:
            if not db.login(userEmail, attrs['old-password']):
                self.set_status(400)
                self.write(dict(errors=[{"title": "old password does not match"}]))
                return
            user['password'] = attrs['password']

        for attr_name in ['name', 'polygon_ids', 'address']:
            if attr_name in attrs:
                user[attr_name] = attrs[attr_name]
        db.update_user(user)
        self.write(dict(data=jsonify_user(user)))

    @tornado.web.authenticated
    def delete(self, userEmail):
        db = self.settings['db']
        if self.current_user['email'] != userEmail:
            self.set_status(404)
            self.write(dict(errors=[{"title": "not found"}]))
            return

        db.delete_user(self.current_user['email'])
        self.set_status(204)


class LoginHandler(BaseHandler):

    @gen.coroutine
    def post(self):
        email = self.get_argument("email")
        password = self.get_argument("password")
        if(self.settings['db'].login(email, password)):
            self.set_secure_cookie("userEmail", email)
            self.write(dict(status="success"))
        else:
            self.set_status(400)
            self.write(dict(status="failure", errors=[{"title": "incorrect email or password"}]))


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("userEmail")
        self.redirect("/")

    def post(self):
        self.clear_cookie("userEmail")
        self.redirect("/")


def jsonify_poly(poly_id, poly):
    return {
        "type": "polygons",
        "id": str(poly_id),
        "attributes": {
            "name": poly["name"],
            "location": poly["location"],
            "start-date": poly["start_date"] and str(poly["start_date"]),
            "end-date": poly["end_date"] and str(poly["end_date"]),
            "poly-type": poly["type"],
        }
    }


class PolyCollectionHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        db = self.settings['db']
        user = self.current_user
        ids = user['polygon_ids']
        polys_json = []
        for poly_id in ids:
            poly = db.get_polygon(str(poly_id), user['email'])
            if poly:
                polys_json += [jsonify_poly(poly_id, poly)]
        self.write({"data": polys_json})

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        db = self.settings['db']
        user = self.current_user
        bodyJSON = tornado.escape.json_decode(self.request.body)
        attr = bodyJSON['data']['attributes']
        poly = db.create_polygon(attr['location'], attr['name'], user['email'], attr['start-date'], attr['end-date'], attr['poly-type'])
        user['polygon_ids'] += [poly['id']]
        db.update_user(user)
        self.write({"data": jsonify_poly(poly['id'], poly)})


class PolyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, poly_id):
        db = self.settings['db']
        poly = db.get_polygon(str(poly_id), self.current_user['email'])
        if(poly is not None):
            self.write({"data": jsonify_poly(poly_id, poly)})
        else:
            self.set_status(404)
            self.write(dict(errors=[{"title": "not found"}]))

    @tornado.web.authenticated
    def patch(self, poly_id):
        db = self.settings['db']
        user = self.current_user
        poly = db.get_polygon(str(poly_id), user['email'])
        if(poly is not None):
            bodyJSON = tornado.escape.json_decode(self.request.body)
            attrs = bodyJSON['data']['attributes']
            for (json_attr, poly_attr) in {
                    'location': 'location',
                    'name': 'name',
                    'start-date': 'start_date',
                    'end-date': 'end_date',
                    'poly-type': 'type'
                    }.items():
                if json_attr in attrs:
                    poly[poly_attr] = attrs[json_attr]
            db.update_polygon(poly)
            self.write({"data": jsonify_poly(poly['id'], poly)})
        else:
            self.set_status(404)
            self.write(dict(errors=[{"title": "not found"}]))

    @tornado.web.authenticated
    def delete(self, poly_id):
        db = self.settings['db']

        user = self.current_user
        if (user['polygon_ids'] and poly_id in user['polygon_ids']):
            user['polygon_ids'].remove(poly_id)
            db.update_user(user)
            db.delete_polygon(poly_id)
            self.set_status(204)
        else:
            self.set_status(404)
            self.write(dict(errors=[{"title": "not found"}]))


def jsonify_poly_type(ptype):
    return {
        "type": "polygon_types",
        "id": ptype["name"],
        "attributes": {
            "is_container": ptype["is_container"],
            "harvest": ptype["harvest"],
            "children": ptype["children"],
        }
    }


class PolyTypeTreeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        db = self.settings['db']
        tree = db.get_poly_type_tree()
        self.write({"data": tree})


class PolyTypeCollectionHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        db = self.settings['db']
        ptypes = db.get_poly_types()
        self.write({"data": [jsonify_poly_type(ptype) for ptype in ptypes]})

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        # TODO: only admins should be able to make new predefined polygon types
        db = self.settings['db']
        bodyJSON = tornado.escape.json_decode(self.request.body)
        name = bodyJSON['data']['id']
        attr = bodyJSON['data']['attributes']
        ptype = db.create_poly_type(name, attr['is_container'], attr['harvest'], attr['children'])
        self.write({"data": jsonify_poly_type(ptype)})


class PolyTypeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, name):
        db = self.settings['db']
        ptype = db.get_poly_type(name)
        if(ptype is not None):
            self.write({"data": jsonify_poly_type(ptype)})
        else:
            self.write({"errors": [{"title": "not found"}]})
            self.set_status(404)

    @tornado.web.authenticated
    def patch(self, name):
        db = self.settings['db']
        ptype = db.get_poly_type(name)
        if(ptype is not None):
            # TODO: only admins should be able to modify predefined polygon types
            bodyJSON = tornado.escape.json_decode(self.request.body)
            attrs = bodyJSON['data']['attributes']
            for attr_name in ['is_container', 'harvest', 'children']:
                if attr_name in attrs:
                    ptype[attr_name] = attrs[attr_name]
            db.update_poly_type(ptype)
            self.write({"data": jsonify_poly_type(ptype)})
        else:
            self.set_status(404)

    @tornado.web.authenticated
    def delete(self, name):
        db = self.settings['db']
        # TODO: only admins should be able to delete predefined polygon types
        ptype = db.get_poly_type(name)
        if(ptype is not None):
            db.delete_poly_type(name)
            self.set_status(204)
        else:
            self.set_status(404)


class Application(tornado.web.Application):
    def __init__(self, database):
        handlers = [
            (r"/api/users", UsersHandler),
            (r"/api/users/(.*)", UsersHandler),
            (r"/api/login", LoginHandler),
            (r"/api/logout", LogoutHandler),
            (r"/api/polygons", PolyCollectionHandler),
            (r"/api/polygons/([0-9]+)", PolyHandler),
            (r"/api/polygon_type_tree", PolyTypeTreeHandler),
            (r"/api/polygon_types", PolyTypeCollectionHandler),
            (r"/api/polygon_types/(.*)", PolyTypeHandler),
            (r"/(favicon.ico)", tornado.web.StaticFileHandler, {"path": os.path.join(os.path.dirname(__file__), "static")}),
            (r"/(assets/.*|ember-welcome-page/.*|fonts/.*|tests/.*|index.html|robots.txt|testem.js)", tornado.web.StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "../ember-proj/dist/"))),
            (r"/.*", MainHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            login_url="/login",
            # TODO: change the cookie secret for production
            cookie_secret=b'\xaf\x07\xee0]DN\xe1R\xac\xd3\xe6\xcbO\xa5\xd7oo\xf9)\xef\xad\xc4L\xbf\xe9\x1c\x93\xfa\xd5\x90\xb9',
            db=database,
        )
        super(Application, self).__init__(handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    db = RiakDb()
    http_server = tornado.httpserver.HTTPServer(Application(db))
    http_server.listen(options.port)
    print("IM RUNNING ON PORT: " + str(options.port))
    tornado.ioloop.IOLoop.current().start()
