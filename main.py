import asyncio
import signal
from multiprocessing import Pool
from os.path import join
from types import FrameType
from typing import Optional

import uvloop

from image_test.config import env_config
from image_test.container.parser_container import ParserContainer
from image_test.image_parser.base import ImageParser


def process_initializer():
    signal.signal(signal.SIGTERM, process_shutdown_handler)


def process_shutdown_handler(signum: int, frame: Optional[FrameType]):
    raise KeyboardInterrupt


def process_start_handler(parser: ImageParser):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(start_app(parser))


async def start_app(parser: type):
    instance = parser()
    pdf_file_path = join(env_config.FILE_PATH, "test.pdf")
    image_dir_path = instance.get_image_dir()
    await instance.extract_images(pdf_file_path, image_dir_path)


if __name__ == "__main__":
    parser_container = ParserContainer()
    parsers = parser_container.Parsers()

    with Pool(processes=len(parsers), initializer=process_initializer) as start_pool:
        start_pool.map(process_start_handler, parsers)
