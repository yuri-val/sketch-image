import os
from typing import Optional
import requests
from requests.exceptions import RequestException


class SketchConverter:
    """A class to convert sketches to images using the WorqHat API."""

    API_URL = "https://api.worqhat.com/api/ai/images/modify/v3/sketch-image"

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the SketchConverter.

        Args:
            api_key (str, optional): The API key for WorqHat. If not provided,
                                     it will be fetched from environment variables.

        Raises:
            ValueError: If the API key is not provided and not found in environment variables.
        """
        self.api_key = api_key or os.getenv("WORQHAT_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set WORQHAT_API_KEY environment variable or pass it to the constructor.")

    def convert_sketch(self, image_path: str, description: str) -> str:
        """
        Convert a sketch to an image using the WorqHat API.

        Args:
            image_path (str): The path to the sketch image file.
            description (str): A description of the desired output image.

        Returns:
            str: The URL of the converted image.

        Raises:
            ValueError: If the sketch conversion fails.
        """
        try:
            response = self._make_api_request(image_path, description)
            return self._extract_image_url(response)
        except RequestException as e:
            raise ValueError(f"Failed to convert sketch: {str(e)}") from e

    def _make_api_request(self, image_path: str, description: str) -> requests.Response:
        """
        Make the API request to convert the sketch.

        Args:
            image_path (str): The path to the sketch image file.
            description (str): A description of the desired output image.

        Returns:
            requests.Response: The API response.

        Raises:
            RequestException: If the API request fails.
        """
        with open(image_path, "rb") as image_file:
            files = {"existing_image": image_file}
            data = {"output_type": "url", "description": description}
            headers = {"Authorization": f"Bearer {self.api_key}"}

            response = requests.post(
                self.API_URL,
                files=files,
                data=data,
                headers=headers
            )
            response.raise_for_status()
            return response

    @staticmethod
    def _extract_image_url(response: requests.Response) -> str:
        """
        Extract the image URL from the API response.

        Args:
            response (requests.Response): The API response.

        Returns:
            str: The URL of the converted image.

        Raises:
            ValueError: If the image URL is not found in the response.
        """
        result = response.json()
        image_url = result.get("image")
        if not image_url:
            raise ValueError("Image URL not found in the API response")
        return image_url
