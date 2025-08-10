from flask import Blueprint, render_template, session, redirect, url_for
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
