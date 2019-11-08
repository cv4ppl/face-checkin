import os

import tornado.options


def init():
    default_tmp_path = "tmp"
    if not os.path.exists(default_tmp_path):
        os.makedirs(default_tmp_path)
    tornado.options.define('port', 8848, type=int, help="port to serve")
    tornado.options.define('db_absl_path', type=str, help="database to load")
    tornado.options.define('data_path', type=str, help="database to load")
    tornado.options.parse_command_line()


def main():
    print("Starting server on port %d" % tornado.options.options.port, flush=True)
    from src.server.server import Server
    Server().run()


if __name__ == '__main__':
    init()
    main()
