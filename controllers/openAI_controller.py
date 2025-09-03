# controllers/openAI_controller.py
from flask import Blueprint, jsonify, request, session
from PIL import Image
from services.openAI_utils import identify_image
from services.image_utils import async_upload
from services.dictionary_utils import fetch_word_info
import threading

openAI_bp = Blueprint("openAI", __name__)

@openAI_bp.route("/analyze", methods=["POST"])
def analyze_upload_image():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    image_file = request.files.get("image")
    if not image_file:
        return jsonify({"error": "No image provided"}), 400

    username = session["username"]
    image = Image.open(image_file.stream).convert("RGB")

    # 1️⃣ GPT nhận diện ảnh
    label_text = identify_image(image).strip().lower().strip(".")
    label_clean = label_text if label_text else "unidentified"

    # 2️⃣ Chạy word_info ở background (không chặn request)
    thread_word = threading.Thread(
        target=fetch_word_info,
        args=(label_clean,),
        daemon=True
    )
    thread_word.start()

    # 3️⃣ Upload ảnh ở background
    thread_upload = threading.Thread(
        target=async_upload,
        args=(username, image.copy(), label_clean),
        daemon=True
    )
    thread_upload.start()

    # 4️⃣ Trả kết quả ngay (chỉ có label)
    return jsonify({
        "label": label_clean,
        "word_info": {}  # word_info sẽ có sau khi DB đã lưu
    })
