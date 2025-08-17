from pathlib import Path

from pdf2image import convert_from_path
from PIL import Image


def pdf_to_images(pdf_path: Path) -> list[Image.Image]:
    return convert_from_path(pdf_path, 500)
