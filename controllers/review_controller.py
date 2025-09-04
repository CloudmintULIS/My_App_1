import os
import uuid
import openai
from dotenv import load_dotenv
from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from models import review_model

# Load .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

review_bp = Blueprint('review', __name__, url_prefix='/review')

@review_bp.route('/')
def review():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    cards = review_model.get_vocab_cards_by_user(user_id)
    return render_template('review.html', cards=cards)

@review_bp.route('/api/delete_card', methods=['POST'])
def delete_card_api():
    card_id = request.json.get('card_id')
    if not card_id:
        return jsonify({"error": "Missing card_id"}), 400

    user_id = session.get('user_id')
    success, error = review_model.delete_card(card_id, user_id)
    return jsonify({"success": success} if success else {"error": error}), 400

@review_bp.route("/api/check_pronounce", methods=["POST"])
def check_pronounce():
    audio_file = request.files.get("audio")
    if not audio_file:
        return jsonify({"result": "Không có audio"}), 400

    os.makedirs("tmp", exist_ok=True)
    file_path = f"tmp/{uuid.uuid4().hex}.wav"
    audio_file.save(file_path)

    try:
        # Gọi Whisper
        with open(file_path, "rb") as f:
            transcript_resp = openai.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
        transcript = transcript_resp.text.strip().lower()

        # Lấy từ gốc từ client
        word = request.form.get("word", "").strip().lower()
        if not word:
            return jsonify({"result": "Không có từ gốc để so sánh"}), 400

        # --- Highlight từng ký tự dựa trên vị trí ---
        highlight_html = ""
        for i, c in enumerate(word):
            if i < len(transcript) and transcript[i] == c:
                highlight_html += f"<span style='color:green;'>{c}</span>"
            else:
                highlight_html += f"<span style='color:red;' title='Bạn phát âm sai'>{c}</span>"

        return jsonify({
            "transcript": transcript,
            "highlight": highlight_html
        })

    except Exception as e:
        return jsonify({"result": f"Lỗi STT: {str(e)}"}), 500

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

