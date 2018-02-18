import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.escape
import tornado.httpclient
#import tornado.AsyncHTTPClient
import os.path
from tornado import gen


from tornado.options import define, options

from storage.riak import RiakDb

define("port", default = 8000, help="run on the given port", type=int)
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("userEmail")

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "localhost:4200")
        self.set_header("Vary","Origin")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", 'PUT, DELETE, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

class MainHandler(BaseHandler):

    def get(self):
        self.render("index.html", error = None)

    @gen.coroutine
    def post(self):
        email = self.get_argument("email")
        name = self.get_argument("name")
        password = self.get_argument("password")

        self.settings['db'].create_user(email,
                       name,
                       password)
        self.set_secure_cookie("userEmail", email)
        self.redirect("/")


class LoginHandler(BaseHandler):

    def get(self):
        self.render("index.html", error = None)

    @gen.coroutine
    def post(self):
        email = self.get_argument("email")
        password = self.get_argument("password")
        if(self.settings['db'].login(email,password)):
            self.set_secure_cookie("userEmail",email)
            self.write(dict(status="success"))
        else:
            self.write(dict(status="failure", error="incorrect email or password"))

class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("userEmail")
        self.redirect("/")

    def post(self):
        self.clear_cookie("userEmail")
        self.redirect("/")


class OtherPagehandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        user = self.settings['db'].get_user(str(self.get_secure_cookie("userEmail"),'utf-8')) #you have to do str(self.get_secure_cookie("cookieName"),'utf-8') to get a string out of a cookie otherwise it returns stupid byte string
        if(not user is None):
            self.render("otherPage.html", user = user['name'], userEmail = user['email'],  pw = user['password'], polygon = None)

        else:
            self.write('<head></head><body>there is no user with that name, it broke</body>')

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        self.settings['db'].create_polygon(self.get_argument("ID"),self.get_argument("Location"),self.get_argument("Name"),str(self.get_secure_cookie("userEmail"),'utf-8'))
        self.redirect("/otherPage")



class GetPolyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.settings['db'].get_user(str(self.get_secure_cookie("userEmail"),'utf-8')) #you have to do str(self.get_secure_cookie("cookieName"),'utf-8') to get a string out of a cookie otherwise it returns stupid byte string
        if(not user is None):
            self.render("otherPage.html", user = user['name'], userEmail = user['email'],  pw = user['password'], polygon = None)

        else:
            self.write('<head></head><body>there is no user with that name, it broke</body>')

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        db = self.settings['db']
        poly = db.get_polygon(self.get_argument("ID"),str(self.get_secure_cookie("userEmail"),'utf-8'))
        user = db.get_user(str(self.get_secure_cookie("userEmail"),'utf-8'))
        if(not user is None):
            if(not poly is None):
                self.render("otherPage.html", user = user['name'], userEmail = user['email'],  pw = user['password'], polygon = poly)
            else:
                self.render("otherPage.html", user = user['name'], userEmail = user['email'],  pw = user['password'], polygon = "Did not exist")

        else:
            self.write('<head></head><body>there is no user with that name, it broke</body>')

class DeletePolyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.settings['db'].get_user(str(self.get_secure_cookie("userEmail"),'utf-8')) #you have to do str(self.get_secure_cookie("cookieName"),'utf-8') to get a string out of a cookie otherwise it returns stupid byte string
        if(not user is None):
            self.render("otherPage.html", user = user['name'], userEmail = user['email'],  pw = user['password'], polygon = None)

        else:
            self.write('<head></head><body>there is no user with that name, it broke</body>')

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        db = self.settings['db']
        db.delete_polygon(self.get_argument("ID"))
        user = db.get_user(str(self.get_secure_cookie("userEmail"),'utf-8'))
        if(not user is None):
            self.render("otherPage.html",user = user['name'], userEmail = user['email'],  pw = user['password'], polygon = "was deleted")

        else:
            self.write('<head></head><body>there is no user with that name, it broke</body>')

class PolyCollectionHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.settings['db'].get_user(str(self.get_secure_cookie("userEmail"),'utf-8')) #you have to do str(self.get_secure_cookie("cookieName"),'utf-8') to get a string out of a cookie otherwise it returns stupid byte string
        if(not user is None):
            self.write(dict(ids=user['polygon_ids']))
        else:
            self.write(dict(error="you are logged in as a nonexistent user"))

    @tornado.web.authenticated
    @gen.coroutine
    def post(self):
        db = self.settings['db']
        user = db.get_user(str(self.get_secure_cookie("userEmail"),'utf-8'))
        # TODO: make sure this is a number, or autogenerate
        poly_id = self.get_argument("ID")
        db.create_polygon(poly_id,self.get_argument("Location"),self.get_argument("Name"), str(self.get_secure_cookie("userEmail"),'utf-8'))
        user['polygon_ids'] += [ poly_id ]
        db.update_user(user)

class PolyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, poly_id):
        db = self.settings['db']
        user = db.get_user(str(self.get_secure_cookie("userEmail"),'utf-8'))
        poly = db.get_polygon(str(poly_id), user['email'])
        if(not user is None):
            if(not poly is None):
                # TODO: verify user owns polygon
                self.write(poly)
            else:
                # TODO: better 404
                self.write(dict(error="not found"))
        else:
            self.write(dict(error="you are logged in as a nonexistent user"))

    @tornado.web.authenticated
    def delete(self, poly_id):
        db = self.settings['db']
        user = db.get_user(str(self.get_secure_cookie("userEmail"),'utf-8'))
        if (user is None):
            self.write(dict(error="you are logged in as a nonexistent user"))
            return

        if (user['polygon_ids']):
            user['polygon_ids'].remove(poly_id)
            db.update_user(user)
            db.delete_polygon(poly_id)
            self.write(dict(status="deleted"))
        else:
            # TODO: http status code
            self.write(dict(error="not your polygon"))


class Application(tornado.web.Application):
    def __init__(self, database):
        handlers =[
            (r"/", MainHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/otherPage",OtherPagehandler),
            (r"/getPoly",GetPolyHandler),
            (r"/deletePoly",DeletePolyHandler),
            (r"/polygons/", PolyCollectionHandler),
            (r"/polygons/([0-9]+)", PolyHandler),
            (r"/(favicon.ico)", tornado.web.StaticFileHandler,{"path": os.path.join(os.path.dirname(__file__))+"/static/favico.ico"})
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
