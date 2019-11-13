import os

from tornado.options import define, parse_command_line

define('port', 8848, int, "port to serve")
define('db_absl_path', os.path.join('data', 'database'), type=str, help="database to load")
define('data_path', 'data', type=str, help="database to load")
parse_command_line()


def main():
    from src.server.server import Server
    Server().run()


if __name__ == '__main__':
    main()
