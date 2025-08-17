from .args import get_args


def main():
    args = get_args()
    print(f"Input file: {args.input}")
    print(f"Output folder: {args.output_folder}")
    print(f"Model: {args.model}")
    print(f"Language: {args.language}")
    print(f"Temperature: {args.temperature}")
    print(f"API Key: {args.api_key}")
    print(f"API Base URL: {args.api_base_url}")


if __name__ == "__main__":
    main()