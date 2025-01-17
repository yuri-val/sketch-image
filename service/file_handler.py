from typing import Dict, Any
from flask import Request


class FileHandler:
    """Handles file-related operations for the application."""

    def get_image_data(self, request: Request) -> str:
        """
        Extract and validate image data from the request.

        Args:
            request (Request): The Flask request object.

        Returns:
            str: The image data.

        Raises:
            ValueError: If the image data is missing or empty.
        """
        data = self._get_json_data(request)
        self._validate_image_data(data)
        return data["image"]

    def _get_json_data(self, request: Request) -> Dict[str, Any]:
        """
        Extract JSON data from the request.

        Args:
            request (Request): The Flask request object.

        Returns:
            Dict[str, Any]: The JSON data from the request.

        Raises:
            ValueError: If the request does not contain valid JSON data.
        """
        data = request.get_json()
        if not data:
            raise ValueError("Invalid JSON data in request")
        return data

    def _validate_image_data(self, data: Dict[str, Any]) -> None:
        """
        Validate the presence and content of image data.

        Args:
            data (Dict[str, Any]): The JSON data from the request.

        Raises:
            ValueError: If the image data is missing or empty.
        """
        if "image" not in data:
            raise ValueError("No image data in request")
        if not data["image"]:
            raise ValueError("Empty image data")