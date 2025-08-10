from flask import Blueprint, render_template, session, redirect, url_for, jsonify
from models import quiz_model
from services import quiz_utils

quiz_bp = Blueprint("quiz", __name__)

@quiz_bp.route("/quiz")
def quiz():
    username = session.get("username")
    if not username:
        return redirect(url_for("auth.login"))

    cards = quiz_model.get_vocab_cards(username)
    quiz_data, error = quiz_utils.generate_quiz(cards)

    if error:
        # Render trang quiz với thông báo lỗi và ẩn phần câu hỏi
        return render_template(
            "quiz.html",
            error_message=error,
            image_path=None,
            choices=[],
            correct_word=None
        )

    return render_template(
        "quiz.html",
        error_message=None,
        image_path=quiz_data["image_path"],
        choices=quiz_data["choices"],
        correct_word=quiz_data["correct_word"]
    )

@quiz_bp.route("/quiz/api/new_quiz")
def new_quiz_api():
    username = session.get("username")
    if not username:
        return jsonify({"error": "Bạn chưa đăng nhập"}), 401

    cards = quiz_model.get_vocab_cards(username)
    quiz_data, error = quiz_utils.generate_quiz(cards)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "image_url": quiz_data["image_path"],
        "choices": quiz_data["choices"],
        "correct_word": quiz_data["correct_word"]
    })
