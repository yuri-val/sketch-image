import base64
import os
from openai import OpenAI

PROMPT = (
    "You are analyzing a hand-drawn sketch that needs to be transformed into a realistic image. Please provide a detailed description that could be used as a prompt for image generation:\n"
    "\n"
    "1. Main Scene Description:\n"
    "- Describe the overall composition and layout\n"
    "- Identify the main focal point and background elements\n"
    "- Specify the perspective and viewing angle\n"
    "- Describe lighting conditions and atmosphere\n"
    "\n"
    "2. Detailed Elements Analysis:\n"
    "- List all objects/subjects present\n"
    "- Describe their exact positions and spatial relationships\n"
    "- Include specific details about textures, materials, and surfaces\n"
    "- Note any color indications (even if sketch is black and white)\n"
    "\n"
    "3. Style Reference:\n"
    "- Mention the desired realistic style (photographic, painterly realistic, etc.)\n"
    "- Suggest material qualities (glossy, matte, rough, smooth)\n"
    "- Describe desired lighting effects and shadows\n"
    "- Include any mood or atmospheric elements\n"
    "\n"
    "4. Important Details:\n"
    "- Highlight any unique features that should be preserved\n"
    "- Specify any textures or patterns\n"
    "- Note any particular details that need enhancement\n"
    "\n"
    "Remember to translate the sketch's simple elements into their realistic counterparts, providing enough detail for accurate image generation.\n"
)


class ImageDescriber:
    def __init__(self, api_key=None):
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def get_description(self, image_path):
        try:
            # Read image file and encode it to base64
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": PROMPT,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=500,
            )

            return response.choices[0].message.content

        except Exception as e:
            raise ValueError(f"Failed to process image: {str(e)}")
