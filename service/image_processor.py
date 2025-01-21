import base64
import os
from datetime import datetime
from typing import Tuple
from PIL import Image
import requests
from io import BytesIO, StringIO
import uuid
import shutil
from markdown import Markdown
from .s3_uploader import S3Uploader


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
        self._md = self._setup_markdown_converter()
        self.s3u = S3Uploader()

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
        image_bytes = self._decode_base64(self._strip_base64_header(image_data))
        filename = self._generate_filename("uploaded_image")
        filepath = self._get_filepath(self.upload_dir, filename)
        self._save_file(filepath, image_bytes, "wb")
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
        self.s3u.upload(filepath, 'generated', filename)
        return filename

    def save_image_data(self, original_path: str, generated_url: str, description: str) -> str:
        """
        Save original image, generated image, and description using a UUID.

        Args:
            original_path (str): Path to the original image.
            generated_url (str): Path to the generated image.
            description (str): Description of the image.

        Returns:
            str: The UUID of the saved data.

        Raises:
            ValueError: If any of the files cannot be saved.
        """
        data_uuid = str(uuid.uuid4())
        base_path = os.path.join("storage", "data", data_uuid)
        os.makedirs(base_path, exist_ok=True)

        try:
            base_s3_path = base_path.replace('storage/', '')

            self._save_and_upload_image(original_path, base_path, base_s3_path, "original.png", copy=True)
            self._save_and_upload_image(generated_url, base_path, base_s3_path, "generated.png", remote=True)
            self._save_and_upload_description(description, base_path, base_s3_path)

            return data_uuid
        except Exception as e:
            raise ValueError(f"Failed to save image data: {str(e)}")

    def _save_and_upload_image(self, source: str, base_path: str, base_s3_path: str, filename: str, copy: bool = False, remote: bool = False):
        """Save and upload an image file."""
        local_path = os.path.join(base_path, filename)
        if copy:
            shutil.copy2(source, local_path)
        elif remote:
            remote_image = self._fetch_remote_image(source)
            remote_image.save(local_path)
        self.s3u.upload(local_path, base_s3_path, filename)

    def _save_and_upload_description(self, description: str, base_path: str, base_s3_path: str):
        """Save and upload description in Markdown and plain text formats."""
        md_path = os.path.join(base_path, "description.md")
        txt_path = os.path.join(base_path, "description.txt")

        self._save_file(md_path, description)
        self._save_file(txt_path, self._strip_markdown(description))

        self.s3u.upload(md_path, base_s3_path, "description.md")
        self.s3u.upload(txt_path, base_s3_path, "description.txt")

    def _strip_markdown(self, text: str) -> str:
        """Strip Markdown formatting from text."""
        return self._md.convert(text)

    @staticmethod
    def _setup_markdown_converter():
        """Set up and return a Markdown converter."""
        def unmark_element(element, stream=None):
            stream = stream or StringIO()
            if element.text:
                stream.write(element.text)
            for sub in element:
                unmark_element(sub, stream)
            if element.tail:
                stream.write(element.tail)
            return stream.getvalue()

        Markdown.output_formats["plain"] = unmark_element
        md = Markdown(output_format="plain")
        md.stripTopLevelTags = False
        return md

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
    def _save_file(filepath: str, content: str | bytes, mode: str = "w") -> None:
        """Save content to a file."""
        with open(filepath, mode, encoding="utf-8" if mode == "w" else None) as f:
            f.write(content)

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