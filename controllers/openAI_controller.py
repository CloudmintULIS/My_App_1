from flask import Blueprint, jsonify, request, session
from PIL import Image
from services.openAI_utils import identify_image
from services.image_utils import async_upload
import threading

openAI_bp = Blueprint("openAI", __name__)
@openAI_bp.route("/analyze", methods=["POST"])
def analyze_upload_image():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    image_file = request.files.get("image")
    if not image_file:
        return jsonify({"error": "No image provided"}), 400

    # Lấy dữ liệu từ session và request ra biến cục bộ
    username = session["username"]

    image = Image.open(image_file.stream).convert("RGB")

    # Gọi GPT để nhận diện
    label_text = identify_image(image)
    label_clean = label_text.replace("This is a ", "").replace("This is an ", "").strip(". ")

    print("Start uploading:", session["username"], label_clean)

    # Khởi chạy thread
    thread = threading.Thread(
        target=async_upload,
        args=(username, image.copy(), label_clean),
        daemon=True  # daemon để không block app khi server shutdown
    )
    thread.start()

    # Trả kết quả nhận diện ngay cho client
    return jsonify({"label": label_text})
