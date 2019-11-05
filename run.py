import os

from tornado.options import define, parse_command_line

from src.server.server import Server

define('port', 8848, int, "port to serve")
define('db_absl_path', os.path.join('data', 'database'), type=str, help="database to load")
define('data_path', 'data', type=str, help="database to load")
parse_command_line()


def init():
    default_tmp_path = "tmp"
    if not os.path.exists(default_tmp_path):
        os.makedirs(default_tmp_path)


def main():
    Server().run()


if __name__ == '__main__':
    init()
    main()
