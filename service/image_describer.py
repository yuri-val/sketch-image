import os
import requests
from typing import Optional

class ImageDescriber:
    """A class to describe images using Worqhat's image analysis API."""

    API_URL = "https://api.worqhat.com/api/ai/content/v4"

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
        self.api_key = api_key or os.getenv("WORQHAT_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Worqhat API key is required. Set it as an environment variable or pass it to the constructor.")

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
            return self._get_ai_description(image_path)
        except Exception as e:
            raise ValueError(f"Failed to process image: {str(e)}")

    def _get_ai_description(self, image_path: str) -> str:
        url = self.API_URL
        payload = {
            'question': self.PROMPT,
            'model': 'aicon-v4-nano-160824',
            'training_data': 'You are analyzing a hand-drawn sketch that needs to be transformed into a realistic image.',
            'stream_data': 'false',
            'response_type': 'text'
        }
        
        with open(image_path, 'rb') as image_file:
            files = [
                ('files', ('sketch.png', image_file, 'image/png'))
            ]
        
            headers = {
                'Authorization': f'Bearer {self.api_key}',
            }

            response = requests.request("POST", url, headers=headers, data=payload, files=files)

            if response.status_code != 200:
                print(f"Error response: {response.status_code}")
                print(f"Response content: {response.text}")
                response.raise_for_status()

            result = response.json()
            if 'content' in result:
                return result['content']
            else:
                raise ValueError(f"Unexpected API response: {result}")