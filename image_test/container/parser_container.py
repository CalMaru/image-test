from dependency_injector import containers, providers

from image_test.config import env_config
from image_test.image_parser.impl.pdf2image_disk import Pdf2ImageDiskParser
from image_test.image_parser.impl.pdf2image_memory import Pdf2ImageMemoryParser
from image_test.image_parser.impl.pdfplumber_disk import PdfplumberDiskImageParser
from image_test.image_parser.impl.pdfplumber_memory import PdfplumberMemoryImageParser
from image_test.image_parser.impl.pdfplumber_memory_chunk import PdfplumberMemoryChunkImageParser
from image_test.image_parser.impl.pymupdf import PyMuPDFImageParser


class ParserContainer(containers.DeclarativeContainer):
    _parsers = [
        Pdf2ImageMemoryParser if env_config.PDF2IMAGE_MEMORY else None,
        Pdf2ImageDiskParser if env_config.PDF2IMAGE_DISK else None,
        PyMuPDFImageParser if env_config.PYMUPDF else None,
        PdfplumberMemoryImageParser if env_config.PDFPLUMBER_MEMORY else None,
        PdfplumberMemoryChunkImageParser if env_config.PDFPLUMBER_MEMORY_CHUNK else None,
        PdfplumberDiskImageParser if env_config.PDFPLUMBER_DISK else None,
    ]

    Parsers = providers.List(*[parser for parser in _parsers if parser is not None])
