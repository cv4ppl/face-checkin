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
    | cid | name | checkin_open | checkin_close |
    --------------------------------------------
    cid: course id
    name: course name
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

    def exist_user(self, username: str, uid: str, password: str, role: str) -> bool:
        if password:
            count = self.__cursor.execute('SELECT * FROM USERS WHERE NAME = ? AND UID = ? AND '
                                          'PASSWORD = ? AND ROLE = ?', (username, uid, password, role))
            return len(count.fetchall()) == 1
        else:
            count = self.__cursor.execute('SELECT * FROM USERS WHERE NAME = ? AND UID = ?', (username, uid))
            return len(count.fetchall()) == 1

    def register_user(self, username: str, uid: str, password: str, role: str) -> None:
        self.__cursor.execute('INSERT INTO USERS (name, uid, password, role) VALUES (?, ?, ?, ?)'
                              , (username, uid, password, role))
        # print(self.__cursor.execute("SELECT * FROM USERS").fetchall())
        self.commit()

    def get_courses(self):
        courses = self.__cursor.execute('SELECT CID, NAME, CHECKIN_OPEN, CHECKIN_CLOSE FROM COURSES').fetchall()
        return courses

    def get_user_records(self, uid):
        records = self.__cursor.execute('SELECT CID, TIME FROM RECORDS WHERE RECORDS.UID = ?', (uid,)).fetchall()
        return records

    def execute_sql(self, sql: str):
        result = self.__cursor.execute(sql).fetchall()
        self.commit()
        return result

    def get_user_ids(self):
        return self.execute_sql("""SELECT uid FROM Users""")

    def get_course_ids(self):
        return self.execute_sql("""SELECT cid FROM Courses""")

    def get_user_by_uid(self, uid: str):
        return self.execute_sql("""SELECT * FROM Users WHERE uid = '%s'""" % uid)

    def get_course_by_cid(self, cid: str):
        return self.execute_sql("""SELECT * FROM Courses WHERE cid = '%s'""" % cid)

    def get_all_records(self):
        return self.execute_sql("""SELECT * FROM Records""")

    def get_records_by_uid(self, uid: str):
        return self.execute_sql("""SELECT * FROM Records WHERE uid = '%s'""" % uid)

    def commit(self):
        self.__conn.commit()
