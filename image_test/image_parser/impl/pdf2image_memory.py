import asyncio
import os
from os.path import join

from pdf2image import convert_from_path

from image_test.image_parser.base import ImageParser
from image_test.logger.log_decorator import time_memory_logger


class Pdf2ImageMemoryParser(ImageParser):
    @time_memory_logger
    async def extract_images(self, pdf_file_path: str, image_dir_path: str) -> None:
        images = await asyncio.to_thread(convert_from_path, pdf_file_path)

        for i, image in enumerate(images, start=1):
            page_dir = join(image_dir_path, str(i))
            os.makedirs(page_dir, exist_ok=True)
            image_path = join(page_dir, f"slide-{i}.png")
            image.save(image_path, "PNG")
