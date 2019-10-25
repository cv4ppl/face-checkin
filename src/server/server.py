"""
Main entrance for starting server
"""
import os

import tornado.ioloop
import tornado.options
import tornado.web

from src.server.backend_service import BackendService
from src.server.upload_handler import UploadHandler
from src.server.login_handler import LoginHandler, ManagerHandler, RegisterHandler

class Server:
    def __init__(self):
        settings = {
            "debug": True,
            "login_url": "/login",
            "cookie_secret": "cv4ppl/face-checkin",
            "template_path": "src" + os.path.sep + "templates",
            "static_path": "src" + os.path.sep + "static",
        }
        self.app = tornado.web.Application([
            ("/login", LoginHandler),
            ("/upload", UploadHandler),
            ("/manage", ManagerHandler),
            ("/register", RegisterHandler)
        ], **settings)
        self.app.listen(tornado.options.options.port)


    def run(self):
        tornado.ioloop.IOLoop.instance().start()
