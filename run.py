import os
import tornado.options

from src.server.server import Server

def init():
    default_tmp_path = "tmp"
    if not os.path.exists(default_tmp_path):
        os.makedirs(default_tmp_path)


def main():
    Server().run()


if __name__ == '__main__':
    init()
    tornado.options.define('port', 8848, int, "port to serve")
    tornado.options.define('db_absl_path', type=str, help="database to load")
    tornado.options.parse_command_line()
    main()
