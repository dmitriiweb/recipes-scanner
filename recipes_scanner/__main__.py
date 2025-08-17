from .args import get_args
from .pdf_scanner import pdf_to_images
from loguru import logger



def main():
    args = get_args()

    logger.info(f"Converting {args.input} to images...")
    images = pdf_to_images(args.input)
    logger.info(f"Converted {len(images)} pages to images")


if __name__ == "__main__":
    main()