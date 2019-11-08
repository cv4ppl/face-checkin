import json
import os

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
        self.set_role(auth_role)
        if auth_role == 'Admin':
            self.redirect("/manage")
        else:
            self.redirect("/upload")


class ManagerHandler(BaseHandler):
    @web.authenticated
    def get(self):
        # TODO(): Base page, show all course with button(redirect dashboard?uid=*&cid=*)
        self.render("../templates/manage.html")
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
        FileManager.write(path, file_metas[0]['body'])
        self.redirect("/")
