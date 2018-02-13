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

define("port", default = 8888, help="run on the given port", type=int)
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("userEmail")

    def set_default_headers(self):
       self.set_header("Access-Control-Allow-Origin", "*")
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

        db.create_user(email,
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
        if(db.login(email,password)):
            self.set_secure_cookie("userEmail",email)
            self.redirect("/otherPage")
        else:
            self.render("index.html",error = "incorrect email or password")

class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("userEmail")
        self.redirect("/")

    def post(self):
        self.clear_cookie("userEmail")
        self.redirect("/")


class CreatePolyhandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,id,location,name):

        user = db.get_user(str(self.get_secure_cookie("userEmail"),'utf-8')) #you have to do str(self.get_secure_cookie("cookieName"),'utf-8') to get a string out of a cookie otherwise it returns stupid byte string
        if(not user is None):
            response = db.create_polygon(id,location,name,user)
            if(not response is None):
                self.write(response)
            else:
                self.write("That poly has already been made.")



class GetPolyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, polyID):
        user = db.get_user(str(self.get_secure_cookie("userEmail"),'utf-8'))
        poly = db.get_polygon(polyID,str(self.get_secure_cookie("userEmail"),'utf-8'))
        if(not user is None):
            if(not poly is None):
                response = {'polygon': poly}
                self.write(response)
            else:
                self.write('<head></head><body>there is no polygon with that ID, it broke</body>')


        else:
            self.write('<head></head><body>there is no user with that name, it broke</body>')

class DeletePolyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,polyID):
        user = db.get_user(str(self.get_secure_cookie("userEmail"),'utf-8')) #you have to do str(self.get_secure_cookie("cookieName"),'utf-8') to get a string out of a cookie otherwise it returns stupid byte string
        if(not user is None):
            response = db.delete_polygon(polyID)
            self.write(response)




class Application(tornado.web.Application):
    def __init__(self):
        handlers =[
            (r"/", MainHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/createPoly/([0-9]+)&([a-z]+)&([a-z]+)",CreatePolyhandler),
            (r"/getPoly/([0-9]+)",GetPolyHandler),
            (r"/deletePoly/([0-9]+)",DeletePolyHandler),
            (r"/(favicon.ico)", tornado.web.StaticFileHandler,{"path": os.path.join(os.path.dirname(__file__))+"/static/favico.ico"})
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            login_url= "/login",
            cookie_secret ="__TODO:__GENERATE__YOUR_OWN_RANDOM_VALUE_HERE:  42",
        )
        super(Application,self).__init__(handlers, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    db = RiakDb()
    print("IM RUNNING ON PORT: " + str( options.port))
    tornado.ioloop.IOLoop.current().start()
