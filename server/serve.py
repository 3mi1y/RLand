import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.escape
import os.path
from tornado import gen


from tornado.options import define, options

from storage.riak import RiakDb

define("port", default = 8000, help="run on the given port", type=int)
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("userEmail")

class MainHandler(BaseHandler):

    def get(self):
        self.render("index.html")
    @gen.coroutine
    def post(self):
        db.create_user(self.get_argument("email"),
                       self.get_argument("name"),
                       self.get_argument("password"))
        self.set_secure_cookie("userEmail", self.get_argument("email"))
        self.redirect("/otherPage")



class OtherPagehandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):

        user = db.get_user(str(self.get_secure_cookie("userEmail"),'utf-8')) #you have to do str(self.get_secure_cookie("cookieName"),'utf-8') to get a string out of a cookie otherwise it returns stupid byte string
        if(not user is None):
            self.render("otherPage.html", user = user['name'], userEmail = user['email'],  pw = user['password'])
        else:
            self.write('<head></head><body>there is no user with that name, it broke</body>')





class Application(tornado.web.Application):
    def __init__(self):
        handlers =[
            (r"/", MainHandler),
            (r"/otherPage",OtherPagehandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            login_url= "/",
            cookie_secret ="__TODO:__GENERATE__YOUR_OWN_RANDOM_VALUE_HERE",
        )
        super(Application,self).__init__(handlers, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    db = RiakDb()
    print("IM RUNNING ON PORT: " + str( options.port))
    tornado.ioloop.IOLoop.current().start()
