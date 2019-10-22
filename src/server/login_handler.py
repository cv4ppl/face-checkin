import hashlib

from src.server.base_handler import BaseHandler

class LoginHandler(BaseHandler):
    def get(self):
        self.render("../templates/login.html")
 
    def post(self):
        # TODO( password -> md5 -> check)
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


class RegisterHandler(BaseHandler):
    def post(self):
        # TODO(): insert (user, md5(user.lower()), md5(password), role) 
        username = self.get_argument("name")
        uid = hashlib.md5(username)
        password = self.get_argument("password")
        role = self.get_argument("role")
        # from backend import ?
        pass


class ManagerHandler(BaseHandler):
    def get(self):
        # TODO(): Base page, show all course with button(redirect dashboard?uid=*&cid=*)
        self.render("../templates/manage.html")
        pass


    def post(self):
        # TODO(): operation    
        #                   -> insert course in Course
        #                   -> delete course (OPTIONAL)
        pass




