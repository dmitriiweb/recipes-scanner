from loguru import logger
from tqdm import tqdm

from .args import get_args
from .pdf_scanner import pdf_to_images
from .ocr import OcrAgent


def main():
    args = get_args()

    args.output_folder.mkdir(parents=True, exist_ok=True)

    logger.info(f"Converting {args.input} to images...")
    images = pdf_to_images(args.input)
    logger.info(f"Converted {len(images)} pages to images")

    logger.info(f"Running OCR agent...")
    ocr_agent = OcrAgent(args)

    logger.info(f"Recognizing images...")
    for image in tqdm(images):
        result = ocr_agent.recognize_image(image)
        if not result.strip():
            continue
        recipe_name = result.split("\n")[0].strip().lstrip("#").strip()
        file_name = f"{recipe_name}.md"
        file_path = args.output_folder / file_name
        with open(file_path, "w") as f:
            f.write(result)




if __name__ == "__main__":
    main()
