"""
Base Handle for auth
Other Handle can inherit BaseHandler to verify auth with
adding @tornado.web.authenticated for get method 
"""
import functools
from typing import Optional, Awaitable, Callable

from tornado.web import RequestHandler
from tornado.web import authenticated


class BaseHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get_current_user(self):
        return self.get_secure_cookie("user")

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
            print(self.get_current_role())
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
