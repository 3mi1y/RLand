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

define("port", default = 8000, help="run on the given port", type=int)
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        cookie_bytes = self.get_secure_cookie("userEmail")
        if not cookie_bytes:
            return None
        return str(cookie_bytes, "utf-8")

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
            self.write(dict(error="user already exists"))

    @tornado.web.authenticated
    def get(self,userEmail):
        db = self.settings['db']
        if self.current_user != userEmail:
            self.set_status(404)
            self.write(dict(error="not found"))
            return

        user = db.get_user(userEmail)
        if(not user is None):
            self.write({"data": jsonify_user(user)})
        else:
            self.write(dict(error="you are logged in as a nonexistent user"))


    @tornado.web.authenticated
    def patch(self,userEmail):
        db = self.settings['db']
        if self.current_user != userEmail:
            self.set_status(404)
            self.write(dict(error="not found"))
            return

        user = db.get_user(userEmail)
        if(not user is None):
            bodyJSON = tornado.escape.json_decode(self.request.body)
            attrs = bodyJSON['data']['attributes']
            if 'email' in attrs and attrs['email'] != userEmail:
                self.write(dict(error = "cannot change user email address"))
                return

            # TODO: should users be able to change their password
            # through this same API?
            for attr_name in ['name', 'polygon_ids', 'address']:
                if attr_name in attrs:
                    user[attr_name] = attrs[attr_name]
            db.update_user(user)
            self.write(dict(data=jsonify_user(user)))
        else:
            self.write(dict(error = "you are logged in as a nonexistent user"))

    @tornado.web.authenticated
    def delete(self, userEmail):
        db = self.settings['db']
        if self.current_user != userEmail:
            self.set_status(404)
            self.write(dict(error="not found"))
            return

        user = db.get_user(userEmail)
        if (user is None):
            self.write(dict(error="you are logged in as a nonexistent user"))
            return

        db.delete_user(userEmail)
        self.set_status(204)


class LoginHandler(BaseHandler):

    @gen.coroutine
    def post(self):
        email = self.get_argument("email")
        password = self.get_argument("password")
        if(self.settings['db'].login(email,password)):
            self.set_secure_cookie("userEmail",email)
            self.write(dict(status="success"))
        else:
            self.set_status(400)
            self.write(dict(status="failure", error="incorrect email or password"))

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
        }
    }

class PolyCollectionHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        db = self.settings['db']
        user = db.get_user(self.current_user)
        if(not user is None):
            ids = user['polygon_ids']
            polys_json = []
            for poly_id in ids:
                poly = db.get_polygon(str(poly_id), user['email'])
                if poly:
                    polys_json += [ jsonify_poly(poly_id, poly) ]
            self.write({ "data": polys_json })
        else:
            self.write(dict(error="you are logged in as a nonexistent user"))

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        db = self.settings['db']
        user = db.get_user(self.current_user)
        bodyJSON = tornado.escape.json_decode(self.request.body)
        attr = bodyJSON['data']['attributes']
        poly = db.create_polygon(attr['location'], attr['name'], self.current_user)
        user['polygon_ids'] += [ poly['id'] ]
        db.update_user(user)
        self.write({"data": jsonify_poly(poly['id'], poly)})

class PolyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, poly_id):
        db = self.settings['db']
        user = db.get_user(self.current_user)
        poly = db.get_polygon(str(poly_id), user['email'])
        if(not user is None):
            if(not poly is None):
                self.write({ "data": jsonify_poly(poly_id, poly) })
            else:
                self.set_status(404)
                self.write(dict(error="not found"))
        else:
            self.write(dict(error="you are logged in as a nonexistent user"))

    @tornado.web.authenticated
    def patch(self, poly_id):
        db = self.settings['db']
        user = db.get_user(self.current_user)
        poly = db.get_polygon(str(poly_id), user['email'])
        if(not user is None):
            if(not poly is None):
                # TODO: verify user owns polygon
                bodyJSON = tornado.escape.json_decode(self.request.body)
                attrs = bodyJSON['data']['attributes']
                for attr_name in ['location', 'name']:
                    if attr_name in attrs:
                        poly[attr_name] = attrs[attr_name]
                db.update_polygon(poly)
                self.write({"data": jsonify_poly(poly['id'], poly)})
            else:
                self.set_status(404)
                self.write(dict(error="not found"))
        else:
            self.write(dict(error="you are logged in as a nonexistent user"))

    @tornado.web.authenticated
    def delete(self, poly_id):
        db = self.settings['db']
        user = db.get_user(self.current_user)
        if (user is None):
            self.write(dict(error="you are logged in as a nonexistent user"))
            return

        if (user['polygon_ids'] and poly_id in user['polygon_ids']):
            user['polygon_ids'].remove(poly_id)
            db.update_user(user)
            db.delete_polygon(poly_id)
            self.set_status(204)
        else:
            self.set_status(404)
            self.write(dict(error="not found"))

def jsonify_poly_type(ptype):
    return {
        "type": "polygon_types",
        "id": ptype["name"],
        "attributes": {
            "is_container": ptype["is_container"],
            "harvest": ptype["harvest"],
            "subtype": ptype["subtype"],
        }
    }

class PolyTypeCollectionHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.set_status(500)

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        # TODO: make sure user is allowed to make new polygon types
        db = self.settings['db']
        bodyJSON = tornado.escape.json_decode(self.request.body)
        name = bodyJSON['data']['id']
        attr = bodyJSON['data']['attributes']
        ptype = db.create_poly_type(name, attr['is_container'], attr['harvest'], attr['subtype'])
        self.write({"data": jsonify_poly_type(ptype)})

class PolyTypeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, name):
        db = self.settings['db']
        ptype = db.get_poly_type(name)
        if(not ptype is None):
            self.write({ "data": jsonify_poly_type(ptype) })
        else:
            self.write({ "error": "not found" })
            self.set_status(404)

    @tornado.web.authenticated
    def patch(self, name):
        db = self.settings['db']
        ptype = db.get_poly_type(name)
        if(not ptype is None):
            # TODO: verify user is allowed to write polygon types
            bodyJSON = tornado.escape.json_decode(self.request.body)
            attrs = bodyJSON['data']['attributes']
            for attr_name in ['is_container', 'harvest', 'subtype']:
                if attr_name in attrs:
                    ptype[attr_name] = attrs[attr_name]
            db.update_poly_type(ptype)
            self.write({"data": jsonify_poly_type(ptype)})
        else:
            self.set_status(404)

    @tornado.web.authenticated
    def delete(self, name):
        db = self.settings['db']
        # TODO: verify user is allowed to delete polygon types
        ptype = db.get_poly_type(name)
        if(not ptype is None):
            db.delete_poly_type(name)
            self.set_status(204)
        else:
            self.set_status(404)



class Application(tornado.web.Application):
    def __init__(self, database):
        handlers =[
            (r"/api/users", UsersHandler),
            (r"/api/users/(.*)",UsersHandler),
            (r"/api/login", LoginHandler),
            (r"/api/logout", LogoutHandler),
            (r"/api/polygons", PolyCollectionHandler),
            (r"/api/polygons/([0-9]+)", PolyHandler),
            (r"/api/polygon_types", PolyTypeCollectionHandler),
            (r"/api/polygon_types/(.*)", PolyTypeHandler),
            (r"/(favicon.ico)", tornado.web.StaticFileHandler,{"path": os.path.join(os.path.dirname(__file__), "static")}),
            (r"/(assets/.*|ember-welcome-page/.*|fonts/.*|tests/.*|index.html|robots.txt|testem.js)", tornado.web.StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "../ember-proj/dist/"))),
            (r"/.*", MainHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            login_url= "/login",
            cookie_secret ="__TODO:__GENERATE__YOUR_OWN_RANDOM_VALUE_HERE:  42",
            db=database,
        )
        super(Application,self).__init__(handlers, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    db = RiakDb()
    http_server = tornado.httpserver.HTTPServer(Application(db))
    http_server.listen(options.port)
    print("IM RUNNING ON PORT: " + str( options.port))
    tornado.ioloop.IOLoop.current().start()
