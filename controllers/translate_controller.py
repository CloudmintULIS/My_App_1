# controllers/translate_controller.py
from flask import Blueprint, request, jsonify
from services.translate_utils import translate_text

translate_bp = Blueprint("translate", __name__)

@translate_bp.route("/api/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text"}), 400

    vi_text = translate_text(text)
    if not vi_text:
        return jsonify({"error": "Translation failed"}), 500

    return jsonify({"translation": vi_text})