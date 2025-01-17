import base64
import os
from datetime import datetime
from typing import Tuple
from PIL import Image
import requests
from io import BytesIO


class ImageProcessor:
    """A class to process and manipulate images."""

    def __init__(self, upload_dir: str = "storage/uploads", generated_dir: str = "storage/generated"):
        """
        Initialize the ImageProcessor.

        Args:
            upload_dir (str): Directory to store uploaded images.
            generated_dir (str): Directory to store generated images.
        """
        self.upload_dir = upload_dir
        self.generated_dir = generated_dir

    def process_base64_image(self, image_data: str) -> str:
        """
        Process a base64 encoded image and save it to the upload directory.

        Args:
            image_data (str): Base64 encoded image data.

        Returns:
            str: The filename of the saved image.

        Raises:
            ValueError: If the base64 string is invalid.
        """
        image_data = self._strip_base64_header(image_data)
        image_bytes = self._decode_base64(image_data)
        filename = self._generate_filename("uploaded_image")
        filepath = self._get_filepath(self.upload_dir, filename)
        self._save_image_bytes(filepath, image_bytes)
        return filename

    def save_generated_image(self, image_path: str, url: str) -> str:
        """
        Combine a local image with a remote image and save the result.

        Args:
            image_path (str): Path to the local image.
            url (str): URL of the remote image.

        Returns:
            str: The filename of the saved combined image.
        """
        local_image = Image.open(image_path)
        remote_image = self._fetch_remote_image(url)
        
        local_image, remote_image = self._resize_images_to_same_height(local_image, remote_image)
        combined_image = self._combine_images(local_image, remote_image)
        
        filename = self._generate_filename("generated_image")
        filepath = self._get_filepath(self.generated_dir, filename)
        combined_image.save(filepath)
        return filename

    @staticmethod
    def _strip_base64_header(image_data: str) -> str:
        """Remove the base64 header if present."""
        return image_data.replace("data:image/png;base64,", "")

    @staticmethod
    def _decode_base64(image_data: str) -> bytes:
        """Decode base64 string to bytes."""
        try:
            return base64.b64decode(image_data)
        except Exception as e:
            raise ValueError("Invalid base64 string") from e

    @staticmethod
    def _generate_filename(prefix: str) -> str:
        """Generate a unique filename with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}_{timestamp}.png"

    @staticmethod
    def _get_filepath(directory: str, filename: str) -> str:
        """Get the full filepath and ensure the directory exists."""
        filepath = os.path.join(directory, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        return filepath

    @staticmethod
    def _save_image_bytes(filepath: str, image_bytes: bytes) -> None:
        """Save image bytes to a file."""
        with open(filepath, "wb") as f:
            f.write(image_bytes)

    @staticmethod
    def _fetch_remote_image(url: str) -> Image.Image:
        """Fetch a remote image from a URL."""
        response = requests.get(url)
        return Image.open(BytesIO(response.content))

    @staticmethod
    def _resize_images_to_same_height(img1: Image.Image, img2: Image.Image) -> Tuple[Image.Image, Image.Image]:
        """Resize two images to have the same height."""
        if img1.size[1] != img2.size[1]:
            height = min(img1.size[1], img2.size[1])
            img1 = img1.resize((int(img1.size[0] * (height / img1.size[1])), height))
            img2 = img2.resize((int(img2.size[0] * (height / img2.size[1])), height))
        return img1, img2

    @staticmethod
    def _combine_images(img1: Image.Image, img2: Image.Image) -> Image.Image:
        """Combine two images side by side."""
        combined_width = img1.size[0] + img2.size[0]
        combined_height = img1.size[1]
        combined_image = Image.new("RGB", (combined_width, combined_height))
        combined_image.paste(img1, (0, 0))
        combined_image.paste(img2, (img1.size[0], 0))
        return combined_image