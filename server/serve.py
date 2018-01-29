import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.escape
import os.path
from tornado import gen
import riak

from tornado.options import define, options

define("port", default = 8000, help="run on the given port", type=int)
class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")
    @gen.coroutine
    def post(self):
        new_user = user_bucket.new('testUser', data ={
                'email': self.get_argument("email"),
                'name': self.get_argument("name"),
                'pw': self.get_argument("password"),
        })
        new_user.store()
        self.redirect("/")



class OtherPagehandler(tornado.web.RequestHandler):
    def get(self):
        user_bucket = client.bucket('user')
        user = user_bucket.get('testUser').data
        self.render("otherPage.html",user = user['name'], userEmail = user['email'],  pw =user['pw'])




class Application(tornado.web.Application):
    def __init__(self):
        handlers =[
            (r"/", MainHandler),
            (r"/otherPage",OtherPagehandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static")
        )
        super(Application,self).__init__(handlers, **settings)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    client = riak.RiakClient()
    user_bucket = client.bucket('user')
    tornado.ioloop.IOLoop.current().start()
