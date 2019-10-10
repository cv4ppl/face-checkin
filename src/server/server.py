"""
Main entrance for starting server
"""

import tornado.ioloop
import tornado.web
from tornado.options import define, options

from src.server.upload_handler import UploadHandler


def main():
    define('port', default=8848, help='run on this port', type=int)
    define('debug', default=True, help='enable debug mode')
    tornado.options.parse_command_line()

    tornado.web.Application([
        ("/upload", UploadHandler),
    ]).listen(options.port)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
