from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
from service.image_processor import ImageProcessor
from service.image_describer import ImageDescriber
from service.sketch_converter import SketchConverter
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
image_processor = ImageProcessor()
image_describer = ImageDescriber()
sketch_converter = SketchConverter()


@app.route("/javascript/<path:filename>")
def serve_js(filename):
    return send_from_directory("static/javascript", filename)


@app.route("/styles/<path:filename>")
def serve_css(filename):
    return send_from_directory("static/styles", filename)


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/magic", methods=["POST"])
def magic():
    data = request.get_json()
    if "image" not in data:
        return jsonify({"error": "No image part"}), 400

    image_data = data["image"]
    if not image_data:
        return jsonify({"error": "No selected file"}), 400

    try:
        filename = image_processor.process_base64_image(image_data)
        filepath = os.path.join(image_processor.upload_dir, filename)
        description = image_describer.get_description(filepath)
        converted_image_url = sketch_converter.convert_sketch(filepath, description)

        image_processor.save_generated_image(filepath, converted_image_url)

        return (
            jsonify(
                {
                    "message": "Image received and processed",
                    "filename": filename,
                    "description": description,
                    "image": converted_image_url,
                }
            ),
            200,
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
