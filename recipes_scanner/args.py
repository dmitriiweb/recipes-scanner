from pathlib import Path
from argparse import ArgumentParser
from dataclasses import dataclass


@dataclass
class Args:
    input: Path
    output_folder: Path
    model: str
    language: str
    temperature: float
    api_key: str | None
    api_base_url: str


def get_args() -> Args:
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", type=Path, required=True, help="Path to the input pdf file")
    parser.add_argument("-o", "--output-folder", type=Path, required=True, help="Path to the output folder")
    parser.add_argument("-m", "--model", type=str, required=False, help="Model to use", default="gemma3:latest")
    parser.add_argument("-l", "--language", type=str, required=False, help="Output language", default="English")
    parser.add_argument("-t", "--temperature", type=float, required=False, help="Temperature", default=0.2)
    parser.add_argument("--api-key", type=str, required=False, help="API key", default=None)
    parser.add_argument("--api-base-url", type=str, required=False, help="API base URL", default="http://localhost:11434")
    
    parsed_args = parser.parse_args()
    return Args(
        input=parsed_args.input,
        output_folder=parsed_args.output_folder,
        model=parsed_args.model,
        language=parsed_args.language,
        temperature=parsed_args.temperature,
        api_key=parsed_args.api_key,
        api_base_url=parsed_args.api_base_url
    )