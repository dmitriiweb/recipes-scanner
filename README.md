### recipes-scanner

Convert one-recipe-per-page PDF cookbooks into clean Markdown using a local vision LLM via Ollama + pydantic-ai.

- **Input**: PDF (each page is a single recipe)
- **Output**: one Markdown file per page in your chosen language
- **Stack**: uv, pydantic-ai, Ollama (OpenAI-compatible), pdf2image, Pillow

---

## Quick start

1) Install prerequisites
- **Python**: 3.12+
- **uv**: see `https://docs.astral.sh/uv/getting-started/`
- **Ollama**: see `https://ollama.com`, then start the server: `ollama serve`

2) Pull a vision model in Ollama (must support image input)
- Recommended: `ollama pull gemma3:latest`

3) Run the CLI with uv
```bash
uv run recipes-scanner \
  -i recipes-example.pdf \
  -o output \
  -m gemma3:latest\
  -l English \
  -t 0.2 \
  --api-base-url http://localhost:11434 \
```
- Output Markdown files are written into `output/`. Each file name is taken from the first `# Heading` line.

---

## CLI
```text
-i, --input            Path to the input pdf file (required)
-o, --output-folder    Path to the output folder (required)
-m, --model            Model to use (default: gemma3:latest)
-l, --language         Output language (default: English)
-t, --temperature      Sampling temperature (default: 0.2)
--api-key              API key (optional; not required for Ollama)
--api-base-url         OpenAI-compatible base URL (default: http://localhost:11434)
```
Notes:
- Use a **vision-capable** model. Text-only models will fail to parse images.
- `--api-key` is accepted for compatibility; Ollama doesn’t need a real key.

---

## How it works
- `pdf2image` converts each PDF page to a high-resolution image (500 DPI).
- `pydantic-ai` `Agent` calls the Ollama OpenAI-compatible endpoint, sending the page image as `BinaryContent`.
- The system prompt instructs the model to return Markdown:
  - `# Dish Name`
  - `## Ingredients` (bullet list)
  - `## Cooking Method` (numbered steps)
  - `## Notes`
- The first Markdown heading becomes the output filename.

---

## Example output
```markdown
# Margherita Pizza

## Ingredients
- 250 g pizza dough
- 100 g tomato sauce
- 125 g mozzarella
- Fresh basil leaves

## Cooking Method
1. Preheat oven to 250°C.
2. Spread sauce on dough, add mozzarella.
3. Bake 8–10 min, garnish with basil.

## Notes
For a crisp base, preheat a pizza stone.
```

---

## Tips and troubleshooting
- **Model not found / image unsupported**: Ensure you pulled a vision model (e.g., `llama3.2-vision:11b`).
- **Poppler missing**: Install Poppler so `pdftoppm` is available.
- **Slow processing**: 500 DPI yields better OCR but is heavier. Consider downscaling pages before `recognize_image` if you customize the code.
- **Weird filenames**: Filenames are derived from the first `# Heading` and not sanitized. If your recipes include characters invalid on your OS, rename files or sanitize in code.
- **Empty outputs**: The agent returns an empty string if it can’t find ingredients and method; such pages are skipped.

---

## Development
- Run directly with uv (no virtualenv activation needed):
  - `uv run recipes-scanner -i input.pdf -o output -m llama3.2-vision:11b`
- Or create a local environment:
  ```bash
  uv sync
  uv run recipes-scanner -i input.pdf -o output -m llama3.2-vision:11b
  ```
- Entry point: `recipes_scanner.__main__:main`
- Key modules:
  - `recipes_scanner/pdf_scanner.py`: PDF → images via `pdf2image`
  - `recipes_scanner/ocr.py`: `OcrAgent` using `pydantic-ai` with Ollama (OpenAI-compatible)
  - `recipes_scanner/args.py`: CLI parsing

---

## License
MIT 
