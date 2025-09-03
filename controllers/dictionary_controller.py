# controllers/word_controller.py
from flask import Blueprint, request, render_template, redirect, flash
from services.dictionary_utils import fetch_word_info
from models.dictionary import save_word_info, get_word_info_from_db

word_bp = Blueprint("word", __name__)

# ===================== Trang lookup =====================
@word_bp.route("/lookup", methods=["GET", "POST"])
def lookup():
    word_data = None
    error = None

    if request.method == "POST":
        word = request.form.get("word", "").strip()
        if not word:
            error = "Vui lòng nhập từ!"
        else:
            # Kiểm tra DB
            word_data = get_word_info_from_db(word)
            if not word_data:
                # Nếu chưa có thì gọi API
                api_data = fetch_word_info(word)
                if api_data:
                    save_word_info(
                        api_data["word"],
                        api_data["phonetic"],
                        api_data["audio"],
                        api_data["definition"],
                        api_data["example"]
                    )
                    word_data = api_data
                else:
                    error = f"Không tìm thấy từ: {word}"

    return render_template("word_lookup.html", word_data=word_data, error=error)
