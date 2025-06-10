import os
from abc import ABCMeta, abstractmethod
from os.path import join

from image_test.config import env_config


class ImageParser(metaclass=ABCMeta):
    def get_image_dir(self) -> str:
        image_dir = join(env_config.FILE_PATH, "result", self.__class__.__name__)
        os.makedirs(image_dir, exist_ok=True)
        return image_dir

    @abstractmethod
    def extract_images(self, pdf_file_path, image_dir_path):
        pass
