import sqlite3
import unittest

import tornado.options

from src.server.backend_service import BackendService


class FaceCheckinSystemTest(unittest.TestCase):
    def setUp(self):
        tornado.options.parse_command_line()
        conn = sqlite3.connect("/var/tmp/test.db")
        cursor = conn.cursor()
        cursor.execute('''DROP TABLE IF EXISTS test_table''')
        cursor.execute('''CREATE TABLE test_table
                        (user_id varchar , name varchar , img_absl_path varchar)''')
        values = [
            ('test_user_id_1', 'test_name_1', 'test_path_1'),
            ('test_user_id_2', 'test_name_2', 'test_path_2'),
            ('test_user_id_3', 'test_name_3', 'test_path_3'),
        ]
        cursor.executemany("""INSERT INTO test_table VALUES (?, ?, ?)""", values)
        conn.commit()
        conn.close()

    def test_backend_service(self):
        self.service = BackendService()
        self.assertEqual(self.service.get_name_by_id("test_table", "test_user_id_1").fetchone()[0], 'test_name_1')
        self.assertEqual(self.service.get_image_path_by_id("test_table", "test_user_id_2").fetchone()[0], 'test_path_2')
        self.assertEqual(self.service.get_column_path_by_id("test_table", "test_user_id_3", "user_id").fetchone()[0],
                         'test_user_id_3')


if __name__ == '__main__':
    tornado.options.options.define('db_absl_path', '/var/tmp/test.db')
    unittest.main()
