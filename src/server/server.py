"""
Main entrance for starting server
"""
import os

import tornado.ioloop
import tornado.options
import tornado.web

from src.server.handlers import UploadHandler, LoginHandler, ManagerHandler, DashboardHandler

class Server:
    def __init__(self):
        settings = {
            "debug": True,
            "login_url": "/login",
            "cookie_secret": "cv4ppl/face-checkin",
            "template_path": os.path.join("src", "templates"),
            "static_path": os.path.join("src", "static"),
        }
        self.app = tornado.web.Application([
            ("/login", LoginHandler),
            ("/upload", UploadHandler),
            ("/manage", ManagerHandler),
            ("/", DashboardHandler)
        ], **settings)
        self.app.listen(tornado.options.options.port)


    def run(self):
        tornado.ioloop.IOLoop.instance().start()
