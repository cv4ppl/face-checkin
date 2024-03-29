"""
Main entrance for starting server
"""
import os

import tornado.ioloop
import tornado.options
import tornado.web

from src.server.backend_service import BackendService
from src.server.handlers import (
    UploadHandler,
    LoginHandler,
    DashboardHandler,
    RegisterHandler,
    CheckInHandler,
    AddCourse,
    ManagerHandler,
    DropCourse,
    DeleteRecord,
    CourseHandler
)


class Server:
    def __init__(self):
        settings = {
            "debug": tornado.options.options.debug,
            "login_url": "/login",
            "cookie_secret": "cv4ppl/face-checkin",
            "template_path": os.path.join("src", "templates"),
            "static_path": os.path.join("src", "static"),
        }
        self.app = tornado.web.Application([
            ("/login", LoginHandler),
            ("/upload", UploadHandler),
            ("/", DashboardHandler),
            ("/register", RegisterHandler),
            ("/checkin", CheckInHandler),
            ("/addCourse", AddCourse),
            ("/manage", ManagerHandler),
            ("/dropCourse", DropCourse),
            ("/deleteRecord", DeleteRecord),
            ("/course", CourseHandler),
        ], **settings)
        self.app.back_service = BackendService()
        self.app.listen(tornado.options.options.port)

    def run(self):
        tornado.ioloop.IOLoop.instance().start()
