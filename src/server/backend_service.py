"""
Backend Service to connect to database.
"""
import sqlite3

import tornado.options


class BackendService:
    """
    Schema of tables.

    -------------------- Users ---------------------
    | uid | name | password | img_absl_path | role |
    ------------------------------------------------
    uid: ID of users including teacher and student
    name: name of user
    password: hashed password
    img_absl_path: avatar of user
    role: admin / teacher / student

    ----------------- Courses ------------------
    | cid | uid | checkin_open | checkin_close |
    --------------------------------------------
    cid: course id
    uid: teacher
    checkin_open: timestamp for checkin to open
    checkin_close: timestamp for checkin to close

    ------------ Records -------------
    | uid | cid | timestamp | status |
    ----------------------------------
    uid: who load the photo
    cid: to which course
    timestamp: when
    status: success / failure
    """

    # TODO(all): feel free to add any method to manipulate database.
    def __init__(self):
        self.__conn = sqlite3.connect(tornado.options.options.db_absl_path)
        self.__cursor = self.__conn.cursor()

    def execute_sql(self, sql: str):
        return self.__cursor.execute(sql).fetchall()

    def get_user_ids(self):
        return self.execute_sql("""SELECT uid FROM Users""")

    def get_course_ids(self):
        return self.execute_sql("""SELECT cid FROM Courses""")

    def get_user_by_uid(self, uid: str):
        return self.execute_sql("""SELECT * FROM Users WHERE uid = %s""" % uid)

    def get_course_by_cid(self, cid: str):
        return self.execute_sql("""SELECT * FROM Courses WHERE cid = %s""" % cid)

    def get_records(self):
        return self.execute_sql("""SELECT * FROM Records""")
