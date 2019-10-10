import tornado.options

from src.server.server import Server


def main():
	Server().run()


if __name__ == '__main__':
	tornado.options.define('port', 8848, int, "port to serve")
	tornado.options.define('db_absl_path', type=str, help="database to load")
	tornado.options.parse_command_line()
	main()
