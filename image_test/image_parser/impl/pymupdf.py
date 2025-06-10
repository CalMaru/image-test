import asyncio
import os
from os.path import join

import fitz

from image_test.config import env_config
from image_test.image_parser.base import ImageParser
from image_test.logger.log_decorator import time_memory_logger


class PyMuPDFImageParser(ImageParser):
    _semaphore = None

    def __init__(self):
        self._semaphore = asyncio.Semaphore(env_config.SEMAPHORE_SIZE)

    @time_memory_logger
    async def extract_images(self, pdf_file_path: str, image_dir_path: str) -> None:
        page_count = self._get_page_count(pdf_file_path)

        tasks = [self.extract_page(pdf_file_path, image_dir_path, page) for page in range(1, page_count + 1)]
        await asyncio.gather(*tasks)

    async def extract_page(self, pdf_file_path: str, image_dir_path: str, page_number: int) -> None:
        async with self._semaphore:

            def read_and_save():
                with fitz.open(pdf_file_path) as doc:
                    page_dir = join(image_dir_path, str(page_number))
                    image_path = join(page_dir, f"slide-{page_number}.png")
                    os.makedirs(page_dir, exist_ok=True)

                    page = doc.load_page(page_number - 1)
                    pix = page.get_pixmap()
                    pix.save(image_path)

            await asyncio.to_thread(read_and_save)

    @staticmethod
    def _get_page_count(pdf_file_path: str) -> int:
        with fitz.open(pdf_file_path) as doc:
            return doc.page_count
