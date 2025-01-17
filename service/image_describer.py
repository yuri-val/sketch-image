import base64
import os
from typing import Optional
from openai import OpenAI

class ImageDescriber:
    """A class to describe images using OpenAI's GPT model."""

    PROMPT = """
    You are analyzing a hand-drawn sketch that needs to be transformed into a realistic image. Please provide a detailed description that could be used as a prompt for image generation:

    1. Main Scene Description:
    - Describe the overall composition and layout
    - Identify the main focal point and background elements
    - Specify the perspective and viewing angle
    - Describe lighting conditions and atmosphere

    2. Detailed Elements Analysis:
    - List all objects/subjects present
    - Describe their exact positions and spatial relationships
    - Include specific details about textures, materials, and surfaces
    - Note any color indications (even if sketch is black and white)

    3. Style Reference:
    - Mention the desired realistic style (photographic, painterly realistic, etc.)
    - Suggest material qualities (glossy, matte, rough, smooth)
    - Describe desired lighting effects and shadows
    - Include any mood or atmospheric elements

    4. Important Details:
    - Highlight any unique features that should be preserved
    - Specify any textures or patterns
    - Note any particular details that need enhancement

    Remember to translate the sketch's simple elements into their realistic counterparts, providing enough detail for accurate image generation.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the ImageDescriber.

        Args:
            api_key (str, optional): The OpenAI API key. If not provided, it will be fetched from environment variables.
        """
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def get_description(self, image_path: str) -> str:
        """
        Get a description of the image at the given path.

        Args:
            image_path (str): The path to the image file.

        Returns:
            str: The description of the image.

        Raises:
            ValueError: If the image processing fails.
        """
        try:
            base64_image = self._encode_image(image_path)
            return self._get_ai_description(base64_image)
        except Exception as e:
            raise ValueError(f"Failed to process image: {str(e)}")

    def _encode_image(self, image_path: str) -> str:
        """
        Encode the image file to base64.

        Args:
            image_path (str): The path to the image file.

        Returns:
            str: The base64 encoded image.
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def _get_ai_description(self, base64_image: str) -> str:
        """
        Get the AI-generated description of the image.

        Args:
            base64_image (str): The base64 encoded image.

        Returns:
            str: The AI-generated description.
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self.PROMPT},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                        },
                    ],
                }
            ],
            max_tokens=500,
        )
        return response.choices[0].message.content