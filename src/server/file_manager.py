"""
Provide file name management
"""

import hashlib
import os
import random


class FileManager:
    def __init__(self):
        self.seed = random.randint()

    @staticmethod
    def get_filename_by_byte_array(ba: bytearray) -> str:
        """
        encoding byte array using md5
        :param ba: byte array
        :return: a string, encoding result of ba
        """
        return hashlib.md5(ba).hexdigest()

    @staticmethod
    def write(path: str, content):
        """

        :param path: filepath
        :param content: file content, usually is a string
        :return: None
        """
        filename = FileManager.get_filename_by_byte_array(bytearray(content))
        with open(os.path.join(path, filename), "wb") as f:
            f.write(bytearray(content))
