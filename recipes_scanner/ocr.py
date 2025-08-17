import io

from PIL import Image
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from .args import AppArgs

DEFAULT_SYSTEM_PROMPT = """
Your task is to parse a recipe from the user's image. 

- Correct grammar mistakes and typos.
- Use {language} as the language of the output text.
- If the image does not ingredients or cooking method, return only empty string.

The answer format should be:

# Dish Name

## Ingredients

- ingredient amount
- ingredient amount

## Cooking Method

1. step 1  
2. step 2  

## Notes

cooking recommendations

"""



class OcrAgent:
    def __init__(self, app_args: AppArgs):
        self.app_args = app_args

        # Define the model with the local Ollama server's base URL
        ollama_model = OpenAIModel(
            model_name=app_args.model,
            provider=OpenAIProvider(
                base_url=f"{app_args.api_base_url}/v1",
                api_key=app_args.api_key or "ollama",  # Ollama doesn't require real API key
            )
        )

        self.ai_agent = Agent(
            model=ollama_model,
            system_prompt=DEFAULT_SYSTEM_PROMPT.format(language=app_args.language),
        )

    def recognize_image(self, image: Image.Image) -> str:
        # Convert PIL Image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format="PNG")
        img_bytes = img_byte_arr.getvalue()

        # Create BinaryContent for the image
        image_content = BinaryContent(data=img_bytes, media_type="image/png")

        # Pass image and prompt to agent
        result = self.ai_agent.run_sync(
            ["Extract a recipe from this image:", image_content]
        )
        return result.output
