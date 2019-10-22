"""
Base Handle for auth
Other Handle can inherit BaseHandler to verify auth with
adding @tornado.web.authenticated for get method 
"""
from tornado.web import RequestHandler

class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

    def set_role(self, fuck):
        #TODO(huchi) : 
        pass