import os

from tornado import web

from src.model.retain_face.detect import predict_by_filename
from src.model.single_face_model import SingleFaceModel
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
import time
from tornado.web import authenticated

single_face_model = SingleFaceModel()


def md5(raw: str):
    return hashlib.md5(raw.encode('utf8')).hexdigest()


class BaseHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get_current_user(self):
        uid = self.get_secure_cookie("uid")
        if uid:
            return uid.decode('utf8')
        return None

    def get_current_role(self):
        return self.get_secure_cookie("role").decode('utf8')

    @staticmethod
    def role_authenticated(
            role, method: Callable[..., Optional[Awaitable[None]]],
            fail_redirect_url: str = '/'
    ) -> Callable[..., Optional[Awaitable[None]]]:
        method = authenticated(method)

        @functools.wraps(method)
        def wrapper(
                self: BaseHandler, *args, **kwargs
        ) -> Optional[Awaitable[None]]:
            if not self.get_current_role() == role:
                return self.redirect(fail_redirect_url)
            return method(self, *args, **kwargs)

        return wrapper

    @staticmethod
    def student_authenticated(
            method: Callable[..., Optional[Awaitable[None]]]
    ) -> Callable[..., Optional[Awaitable[None]]]:
        return BaseHandler.role_authenticated(role='Student', method=method)

    @staticmethod
    def admin_authenticated(
            method: Callable[..., Optional[Awaitable[None]]]
    ) -> Callable[..., Optional[Awaitable[None]]]:
        return BaseHandler.role_authenticated(role='Admin', method=method)


class ManagerHandler(BaseHandler):
    @web.authenticated
    def get(self):
        # TODO(): Base page, show all course with button(redirect dashboard?uid=*&cid=*)
        courses = self.application.back_service.get_courses()
        courses = sorted(courses)
        record_id = 0
        courses_records = []
        for course in courses:
            courses_records.append({
                "cid": course[0],
                "name": course[1]
            })
        self.render("manage.html", courses=courses_records)
        pass

    @web.authenticated
    def post(self):
        # TODO(): operation
        #                   -> insert course in Course
        #                   -> delete course (OPTIONAL)
        pass


class UploadHandler(BaseHandler):
    @web.authenticated
    def post(self):
        cid = int(self.get_argument("cid"))
        for uid in self.get_arguments("uid"):
            global_backend_service.execute_sql(
                """INSERT INTO Records VALUES ('%s', %d, %d, true)""" % (uid, cid, int(time.time() * 1000))
            )
        self.redirect('/')


class DashboardHandler(BaseHandler):
    @web.authenticated
    def get(self):
        uid = self.get_current_user()
        user = global_backend_service.get_user_by_uid(uid)[0]

        assert user[-1] in ("Admin", "Student")
        if user[-1] == "Admin":
            valid_list = global_backend_service.get_all_records()
        else:
            valid_list = global_backend_service.get_records_by_uid(user[0])

        stringed_list = []

        for item in valid_list:
            stringed_list.append({
                "username": global_backend_service.get_user_by_uid(item[0])[0][1],
                "course": global_backend_service.get_course_by_cid(item[1])[0][1],
                "time": item[2] // 1000,
                "color": "green" if item[3] else "red"
            })

        self.render(
            template_name="dashboard.html",
            username=user[1],
            records=stringed_list,
            admin=(self.get_current_role() == "Admin")
        )


class LoginHandler(BaseHandler):
    def get(self):
        logout = int(self.get_argument("logout", "0"))
        if logout:
            self.clear_all_cookies()
            self.redirect("/")
            return
        register = int(self.get_argument("new", default="0"))
        if register:
            username = self.get_argument("username", default="")
            self.render("register.html", username=username)
            return
        if self.get_current_user():
            self.redirect("/")
            return
        self.render("login.html")

    def post(self):
        register = int(self.get_argument("new", "0"))
        username = self.get_argument("username")
        uid = md5(username.lower())
        password = self.get_argument("password")
        if register:
            role = self.get_argument("role")
            user = global_backend_service.get_user_by_uid(uid)
            if user:
                self.redirect(self.get_login_url() + "?new=1&username=%s" % username)
                return
            else:
                self.application.back_service.register_user(username, uid, password, role)
                self.clear_all_cookies()
                self.set_secure_cookie("uid", uid)
                self.set_secure_cookie("role", role)
        else:
            user = global_backend_service.get_user_by_uid(uid)
            if len(user):
                user = user[0]
                if user[2] == password:
                    self.set_secure_cookie(
                        name="uid",
                        value=uid,
                    )
                    self.set_secure_cookie("role", user[4])
                else:
                    self.redirect(self.get_login_url())
                    return
            else:
                self.redirect(self.get_login_url() + "?new=1&username=%s" % username)
                return
        self.redirect(self.get_argument("next", "/"))


class RegisterHandler(BaseHandler):
    def post(self):
        username = self.get_argument("name")
        uid = hashlib.md5(username.encode('utf-8')).hexdigest()
        password = self.get_argument("password")
        role = self.get_argument("registerRole")
        if self.application.back_service.exist_user(username, uid, None, None):
            return self.render('login.html', info={"ERROR": "用户名已存在"})
        self.render('login.html', info={"WELCOME": "注册完请登录"})


class AddCourse(BaseHandler):

    @BaseHandler.admin_authenticated
    def post(self):
        course_name = self.get_argument("name")
        self.application.back_service.add_course(course_name)
        return self.redirect('/manage')


class CheckInHandler(BaseHandler):
    @web.authenticated
    def get(self):
        uid = self.get_secure_cookie("uid")
        courses = self.application.back_service.get_courses()
        records = self.application.back_service.get_user_records(uid)
        courses = sorted(courses)
        records = sorted(records)
        record_id = 0
        courses_records = []
        print(records)

        for course in courses:
            is_checkin = False
            for record in records:
                if record[0] == course[0]:
                    is_checkin = True
                    break
            courses_records.append({
                "cid": course[0],
                "name": course[1],
                # "checkin_num"
                "is_checkin": is_checkin,
                "disabled": "disabled" if is_checkin else ""
            })
            record_id += is_checkin
        self.render('checkin.html', courses=courses_records)

    def post(self):
        cid = int(self.get_argument("cid"))
        file_metas = self.request.files.get("image", None)
        if not file_metas or len(file_metas) != 1:
            self.redirect("checkin")
            return

        path = "/var/tmp" if os.path.exists('/var/tmp') else os.curdir + os.path.sep + 'tmp'
        filename = FileManager.write(path, file_metas[0]['body'])

        faces = predict_by_filename(filename)
        ok = []
        for face, file in faces:
            possibility = single_face_model.get_id_by_image(face)
            ok.append((possibility, file))
        uid_to_name = dict()
        all_users = global_backend_service.get_all_users()
        for u in all_users:
            uid_to_name[u[0]] = u[1]
        self.render("upload.html", possible_users=ok, uid_to_name=uid_to_name, cid=cid)


class DropCourse(BaseHandler):
    @BaseHandler.admin_authenticated
    def get(self):
        cid = self.get_argument('cid')
        self.application.back_service.delete_course(cid)
        return self.redirect('/manage')
