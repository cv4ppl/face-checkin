"""
Main entrance for starting server
"""

import tornado.ioloop
import tornado.options
import tornado.web

from src.server.upload_handler import UploadHandler


class Server:
    def __init__(self):
        self.app = tornado.web.Application([
            ("/upload", UploadHandler),
        ])
        self.app.listen(tornado.options.options.port)

    def run(self):
        tornado.ioloop.IOLoop.instance().start()
