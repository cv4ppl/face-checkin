"""
Handle request to ":/upload"
get method will render the upload page,
post method will do uploading action.
"""

import json
import os
from typing import Optional, Awaitable

from tornado.web import RequestHandler

from src.server.file_manager import FileManager


class UploadHandler(RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def get(self):
        return self.render("../templates/upload.html")

    def post(self):
        file_metas = self.request.files.get("image", None)
        if not file_metas or len(file_metas) != 1:
            self.write(json.dumps({
                'result': 'Failed',
            }))
            return

        path = "/var/tmp" if os.path.exists('/var/tmp') else os.curdir + os.path.sep + 'tmp'
        FileManager.write(path, file_metas[0]['body'])

        self.write(json.dumps({
            'result': 'OK',
        }))
