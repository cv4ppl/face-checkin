"""
Main entrance for starting server
"""

import argparse

import tornado.ioloop
import tornado.web

from src.server.upload_handler import UploadHandler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8848)
    args = parser.parse_args()

    tornado.web.Application([
        ("/upload", UploadHandler),
    ]).listen(args.port)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
