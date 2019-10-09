"""
Handle request to ":/upload"
get method will render the upload page,
post method will do uploading action.
"""

import json
import os

from tornado.web import RequestHandler

from src.server.file_manager import FileManager


class UploadHandler(RequestHandler):
    def get(self):
        return self.render("../templates/upload.html")

    def post(self):
        file_metas = self.request.files.get("image", None)
        if not len(file_metas) == 1:
            self.write(json.dumps({
                'result': 'Failed',
            }))

        path = "/var/tmp" if os.path.exists('/var/tmp') else os.curdir + os.pathsep + 'tmp'
        FileManager.write(path, file_metas[0]['body'])

        self.write(json.dumps({
            'result': 'OK',
        }))
