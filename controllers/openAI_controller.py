from flask import Blueprint, jsonify, request, session
from PIL import Image
from services.openAI_utils import identify_image
from services.image_utils import upload_image_and_save

openAI_bp = Blueprint("openAI", __name__)

@openAI_bp.route("/analyze", methods=["POST"])
def analyze_image():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    image_file = request.files.get("image")
    if not image_file:
        return jsonify({"error": "No image provided"}), 400

    image = Image.open(image_file.stream).convert("RGB")

    label_text = identify_image(image)
    label_clean = label_text.replace("This is a ", "").replace("This is an ", "").strip(". ")

    upload_image_and_save(session["username"], image, label_clean)

    return jsonify({"label": label_text})
