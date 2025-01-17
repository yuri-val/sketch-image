import base64
import os
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO


class ImageProcessor:
    def __init__(self, upload_dir="storage/uploads", generated_dir="storage/generated"):
        self.upload_dir = upload_dir
        self.generated_dir = generated_dir

    def process_base64_image(self, image_data):
        if image_data.startswith("data:image/png;base64,"):
            image_data = image_data.replace("data:image/png;base64,", "")

        try:
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            raise ValueError("Invalid base64 string")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"uploaded_image_{timestamp}.png"
        filepath = os.path.join(self.upload_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "wb") as f:
            f.write(image_bytes)

        return filename

    def save_generated_image(self, image_path, url):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"generated_image_{timestamp}.png"
        filepath = os.path.join(self.generated_dir, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        local_image = Image.open(image_path)

        # Fetch the remote image
        response = requests.get(url)
        remote_image = Image.open(BytesIO(response.content))

        # Ensure both images have the same height
        if local_image.size[1] != remote_image.size[1]:
            # Resize the images to have the same height
            height = min(local_image.size[1], remote_image.size[1])
            local_image = local_image.resize(
                (int(local_image.size[0] * (height / local_image.size[1])), height)
            )
            remote_image = remote_image.resize(
                (int(remote_image.size[0] * (height / remote_image.size[1])), height)
            )

        # Create a new blank image with the combined width
        combined_width = local_image.size[0] + remote_image.size[0]
        combined_height = local_image.size[1]
        combined_image = Image.new("RGB", (combined_width, combined_height))

        # Paste the local image on the left
        combined_image.paste(local_image, (0, 0))

        # Paste the remote image on the right
        combined_image.paste(remote_image, (local_image.size[0], 0))

        # Save the combined image
        combined_image.save(filepath)
