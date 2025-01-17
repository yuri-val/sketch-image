from flask import Flask, request, jsonify, send_from_directory
from service.image_processor import ImageProcessor
from service.image_describer import ImageDescriber
from service.sketch_converter import SketchConverter
from service.file_handler import FileHandler
from dotenv import load_dotenv
import os
from typing import Tuple, Dict, Any

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")

class ImageProcessingService:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.image_describer = ImageDescriber()
        self.sketch_converter = SketchConverter()
        self.file_handler = FileHandler()

    def process_image(self, request_data) -> Tuple[Dict[str, Any], int]:
        try:
            image_data = self.file_handler.get_image_data(request_data)
            filename = self.image_processor.process_base64_image(image_data)
            filepath = os.path.join(self.image_processor.upload_dir, filename)
            
            description = self.image_describer.get_description(filepath)
            converted_image_url = self.sketch_converter.convert_sketch(filepath, description)
            
            self.image_processor.save_generated_image(filepath, converted_image_url)

            uuid = self.image_processor.save_image_data(filepath, converted_image_url, description)
            
            return {
                "message": "Image received and processed",
                "filename": filename,
                "description": description,
                "image": converted_image_url,
                "uuid": uuid,
            }, 200
        except ValueError as e:
            return {"error": str(e)}, 400

image_processing_service = ImageProcessingService()

@app.route("/assets/<path:filename>")
def serve_static(filename: str):
    """Serve static files from their respective directories."""
    return send_from_directory("static", filename)

@app.route("/")
def index():
    """Serve the main index.html file."""
    return send_from_directory("static", "index.html")

@app.route("/magic", methods=["POST"])
def magic():
    """Process the uploaded image and return the result."""
    result, status_code = image_processing_service.process_image(request)
    return jsonify(result), status_code

if __name__ == "__main__":
    app.run(host="localhost", debug=True)