import asyncio
import os
from os.path import join

import pdfplumber
from pdf2image import convert_from_path

from image_test.config import env_config
from image_test.image_parser.base import ImageParser
from image_test.logger.log_decorator import time_memory_logger


class PdfplumberMemoryImageParser(ImageParser):
    _semaphore = None

    def __init__(self):
        self._semaphore = asyncio.Semaphore(env_config.SEMAPHORE_SIZE)

    @time_memory_logger
    async def extract_images(self, pdf_file_path: str, image_dir_path: str) -> None:
        page_count = self._get_page_count(pdf_file_path)

        tasks = [self._save_images(pdf_file_path, image_dir_path, page + 1) for page in range(page_count)]
        await asyncio.gather(*tasks)

    async def _save_images(self, pdf_file_path: str, image_dir_path: str, page: int) -> None:
        async with self._semaphore:
            images = await asyncio.to_thread(convert_from_path, pdf_file_path, first_page=page, last_page=page)

            page_dir = join(image_dir_path, str(page))
            os.makedirs(page_dir, exist_ok=True)

            image_path = join(page_dir, f"slide-{page}.png")
            images[0].save(image_path, "PNG")

    @staticmethod
    def _get_page_count(pdf_file_path: str) -> int:
        with pdfplumber.open(pdf_file_path) as pdf:
            return len(pdf.pages)
