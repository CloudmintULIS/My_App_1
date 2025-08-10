from flask import Blueprint, request, jsonify, session
from PIL import Image
from services.image_utils import upload_image_and_save

image_bp = Blueprint("image", __name__)

@image_bp.route("/upload", methods=["POST"])
def upload_vocab_image():
    if "username" not in session:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    username = session["username"]

    # Giả sử bạn gửi ảnh dưới dạng base64 hoặc file, xử lý lấy ảnh PIL
    file = request.files.get("image")
    if not file:
        return jsonify({"success": False, "error": "No image provided"}), 400

    image = Image.open(file.stream)

    label_clean = request.form.get("label", "").strip()
    if not label_clean:
        return jsonify({"success": False, "error": "No label provided"}), 400

    success, image_url, error = upload_image_and_save(username, image, label_clean)
    if success:
        return jsonify({"success": True, "image_url": image_url})
    else:
        return jsonify({"success": False, "error": error})
