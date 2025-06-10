import asyncio
import os
from os.path import join

import pdfplumber
from pdf2image import convert_from_path

from image_test.config import env_config
from image_test.image_parser.base import ImageParser
from image_test.logger.log_decorator import time_memory_logger


class PdfplumberMemoryChunkImageParser(ImageParser):
    _semaphore = None

    def __init__(self):
        self._semaphore = asyncio.Semaphore(env_config.SEMAPHORE_SIZE)

    @time_memory_logger
    async def extract_images(self, pdf_file_path: str, image_dir_path: str) -> None:
        page_count = self._get_page_count(pdf_file_path)
        chunk_ranges = self._get_chunk_ranges(page_count)

        tasks = [self._save_images(pdf_file_path, image_dir_path, start, end) for start, end in chunk_ranges]
        await asyncio.gather(*tasks)

    async def _save_images(self, pdf_file_path: str, image_dir_path: str, start: int, end: int) -> None:
        async with self._semaphore:
            images = await asyncio.to_thread(convert_from_path, pdf_file_path, first_page=start, last_page=end)

            for i, image in enumerate(images, start=start):
                page_dir = join(image_dir_path, str(i))
                os.makedirs(page_dir, exist_ok=True)
                image_path = join(page_dir, f"slide-{i}.png")
                image.save(image_path, "PNG")

    @staticmethod
    def _get_page_count(pdf_file_path: str) -> int:
        with pdfplumber.open(pdf_file_path) as pdf:
            return len(pdf.pages)

    @staticmethod
    def _get_chunk_ranges(page_count: int) -> list[tuple[int, int]]:
        chunk_ranges = []

        for start in range(1, page_count + 1, env_config.CHUNK_SIZE):
            end = min(start + env_config.CHUNK_SIZE - 1, page_count)
            chunk_ranges.append((start, end))

        return chunk_ranges
