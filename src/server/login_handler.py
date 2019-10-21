
from src.server.base_handler import BaseHandler

class LoginHandler(BaseHandler):
    def get(self):
        self.render("../templates/login.html")
 
    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        # TODO(redirect Teacher and Student home page with password)
        self.redirect("/upload")

