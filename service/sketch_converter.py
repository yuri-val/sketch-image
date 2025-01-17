import os
import requests



class SketchConverter:
    def __init__(self, api_key=None):
        if not api_key:
            api_key = os.getenv("WORQHAT_API_KEY")
        self.api_key = api_key
        self.api_url = "https://api.worqhat.com/api/ai/images/modify/v3/sketch-image"

    def convert_sketch(self, image_path, description):
        try:
            with open(image_path, "rb") as image_file:
                files = {"existing_image": image_file}
                data = {"output_type": "url", "description": description}
                headers = {"Authorization": f"Bearer {self.api_key}"}

                response = requests.post(
                    self.api_url, files=files, data=data, headers=headers
                )
                response.raise_for_status()
                result = response.json()

                return result.get("image")

        except Exception as e:
            raise ValueError(f"Failed to convert sketch: {str(e)}")
