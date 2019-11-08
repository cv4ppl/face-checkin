import json
import os
import time
import cv2
import datetime
from tornado import web

from src.server.backend_service import BackendService
from src.server.file_manager import FileManager

global_backend_service = BackendService()


class BaseHandler(web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        passwd = self.get_argument("passwd")
        print(passwd)
        auth_role = self.get_argument("role")
        # check auth_role legal (need move to front end)
        if auth_role not in ("Admin", "Student"):
            self.redirect("/login")
        if auth_role == 'Admin':
            self.redirect("/manage")
        else:
            self.redirect("/upload")


class ManagerHandler(BaseHandler):
    @web.authenticated
    def get(self):
        # TODO(): Base page, show all course with button(redirect dashboard?uid=*&cid=*)
        self.render("manage.html")
        pass

    @web.authenticated
    def post(self):
        # TODO(): operation    
        #                   -> insert course in Course
        #                   -> delete course (OPTIONAL)
        pass


class UploadHandler(BaseHandler):
    @web.authenticated
    def get(self):
        return self.render("upload.html")

    @web.authenticated
    def post(self):
        file_metas = self.request.files.get("image", None)
        if not file_metas or len(file_metas) != 1:
            self.write(json.dumps({
                'result': 'Failed',
            }))
            return

        path = "/var/tmp" if os.path.exists('/var/tmp') else os.curdir + os.path.sep + 'tmp'
        filename = FileManager.write(path, file_metas[0]['body'])
        cv2.imread(os.path.join(path, filename))
        self.redirect("/")

class DashboardHandler(BaseHandler):
    # @web.authenticated
    def get(self):
        uid = self.get_current_user()
        uid = "1"
        user = global_backend_service.get_user_by_uid(uid)[0]

        assert user[-1] in ("admin", "student")
        if user[-1] == "admin":
            valid_list = global_backend_service.get_all_records()
        else:
            valid_list = global_backend_service.get_user_by_uid(user[0])

        stringed_list = []

        for item in valid_list:
            print(global_backend_service.get_course_by_cid(item[1]))
            print(item[2])
            stringed_list.append({
                "username": global_backend_service.get_user_by_uid(item[0])[0][1],
                "course": global_backend_service.get_course_by_cid(item[1])[0][1],
                "time": datetime.datetime.fromtimestamp(item[2] / 1000.0),
                "color": "green" if item[3] else "red"
            })

        self.render(
            template_name="dashboard.html",
            username=user[1],
            records=stringed_list,
        )