import sqlite3

import tornado.options


class BackendService:
    def __init__(self):
        self.__conn = sqlite3.connect(tornado.options.options.db_absl_path)

    def get_column_path_by_id(self, table_name: str, user_id: str, column: str):
        return self.__conn.execute(
            "SELECT %s FROM %s WHERE user_id = '%s'" % (column, table_name, user_id))

    def get_name_by_id(self, table_name: str, user_id: str):
        return self.get_column_path_by_id(table_name, user_id, "name")

    def get_image_path_by_id(self, table_name: str, user_id: str):
        return self.get_column_path_by_id(table_name, user_id, "img_absl_path")
