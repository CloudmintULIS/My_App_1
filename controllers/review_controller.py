from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from models import review_model
from services import review_utils

review_bp = Blueprint('review', __name__, url_prefix='/review')

@review_bp.route('/')
def review():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    cards = review_model.get_vocab_cards_by_user(user_id)
    cards = review_utils.prepare_cards_for_review(cards)

    return render_template('review.html', cards=cards)

@review_bp.route('/api/delete_card', methods=['POST'])
def delete_card_api():
    card_id = request.json.get('card_id')

    if not card_id:
        return jsonify({"error": "Missing card_id"}), 400

    # Xóa chỉ thẻ của user hiện tại
    user_id = session.get('user_id')
    success, error = review_model.delete_card(card_id, user_id)

    if success:
        return jsonify({"success": True})
    else:
        return jsonify({"error": error}), 400
