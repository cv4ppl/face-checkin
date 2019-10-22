"""
Model to map the face image to id, where id is provided by database.
"""

from src.server.backend_service import BackendService


class DataProvider:
    def __init__(self):
        self.backend_service = BackendService()

    # def get_images(self):


class SingleFaceModel:
    def get_id_by_image(self, img):
        # TODO(#6): currently returns fake id,
        #  will be implemented by Han and Jiacheng.
        return "this-is-a-fake-id"
