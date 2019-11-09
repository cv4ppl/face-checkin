import datetime
import json
import os

import cv2
from tornado import web

from src.server.backend_service import BackendService
from src.server.file_manager import FileManager

global_backend_service = BackendService()

"""
Base Handle for auth
Other Handle can inherit BaseHandler to verify auth with
adding @tornado.web.authenticated for get method 
"""
import functools
from typing import Optional, Awaitable, Callable
import hashlib
from tornado.web import RequestHandler
from tornado.web import authenticated


class BaseHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get_current_user(self):
        uid = self.get_secure_cookie("uid")
        if uid:
            return uid.decode('utf8')
        return None

    def get_current_role(self):
        return self.get_secure_cookie("role")

    @staticmethod
    def role_authenticated(
            role, method: Callable[..., Optional[Awaitable[None]]],
            fail_redirect_url: str = '/login'
    ) -> Callable[..., Optional[Awaitable[None]]]:
        method = authenticated(method)

        @functools.wraps(method)
        def wrapper(
                self: BaseHandler, *args, **kwargs
        ) -> Optional[Awaitable[None]]:
            if not self.get_current_role().decode() == role:
                return self.redirect(fail_redirect_url)
            return method(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def student_authenticated(
            method: Callable[..., Optional[Awaitable[None]]]
    ) -> Callable[..., Optional[Awaitable[None]]]:
        return BaseHandler.role_authenticated(role='Student', method=method)

    @staticmethod
    def admin_authentiated(
            method: Callable[..., Optional[Awaitable[None]]]
    ) -> Callable[..., Optional[Awaitable[None]]]:
        return BaseHandler.role_authenticated(role='Admin', method=method)

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
        img = cv2.imread(os.path.join(path, filename))

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


class LoginHandler(BaseHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        self.clear_all_cookies()
        self.render("login.html", info={"WELCOME": "欢迎登陆"})

    def post(self):
        username = self.get_argument("name")
        uid = hashlib.md5(username.encode('utf-8')).hexdigest()
        password = self.get_argument("password")
        auth_role = self.get_argument("role")
        if not self.application.back_service.exist_user(username, uid, password, auth_role):
            return self.render('login.html', info={"ERROR": "密码错误"})
        self.set_secure_cookie("user", username)
        self.set_secure_cookie("uid", uid)
        self.set_secure_cookie("role", auth_role)
        self.redirect("/manage" if auth_role == 'Admin' else "/upload")


class RegisterHandler(BaseHandler):
    def post(self):
        # TODO(): insert (user, md5(user.lower()), md5(password), role)
        username = self.get_argument("name")
        uid = hashlib.md5(username.encode('utf-8')).hexdigest()
        password = self.get_argument("password")
        role = self.get_argument("registerRole")
        if self.application.back_service.exist_user(username, uid, None, None):
            return self.render('login.html', info={"ERROR": "用户名已存在"})
        self.application.back_service.register_user(username, uid, password, role)
        self.render('login.html', info={"WELCOME": "注册完请登录"})


class ManagerHandler(BaseHandler):
    @BaseHandler.admin_authentiated
    def get(self):
        # TODO(): Base page, show all course with button(redirect dashboard?uid=*&cid=*)
        # print(self.get_current_role())
        # if self.get_current_role() == b'Student':
        #     return self.redirect("/upload")
        self.render("manage.html")
        pass

    def post(self):
        # TODO(): operation
        #                   -> insert course in Course
        #                   -> delete course (OPTIONAL)
        pass
