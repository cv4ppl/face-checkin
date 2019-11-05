import hashlib
from typing import Optional, Awaitable

import tornado

from src.server.base_handler import BaseHandler


class LoginHandler(BaseHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        self.clear_all_cookies()
        self.render("../templates/login.html", info={"WELCOME": "欢迎登陆"})

    def post(self):
        username = self.get_argument("name")
        uid = hashlib.md5(username.encode('utf-8')).hexdigest()
        password = self.get_argument("password")
        auth_role = self.get_argument("role")
        if not self.application.back_service.exist_user(username, uid, password, auth_role):
            return self.render('../templates/login.html', info={"ERROR": "密码错误"})
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
            return self.render('../templates/login.html', info={"ERROR": "用户名已存在"})
        self.application.back_service.register_user(username, uid, password, role)
        self.render('../templates/login.html', info={"WELCOME": "注册完请登录"})


class ManagerHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        # TODO(): Base page, show all course with button(redirect dashboard?uid=*&cid=*)
        print(self.get_current_role())
        if self.get_current_role() == b'Student':
            return self.redirect("/upload")
        self.render("../templates/manage.html")
        pass

    def post(self):
        # TODO(): operation    
        #                   -> insert course in Course
        #                   -> delete course (OPTIONAL)
        pass




