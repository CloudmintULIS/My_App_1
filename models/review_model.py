import psycopg2.extras
from models.db import get_db_connection

def get_vocab_cards_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute(
        "SELECT * FROM vocab_cards WHERE user_id = %s ORDER BY timestamp DESC",
        (user_id,)
    )
    cards = cursor.fetchall()
    cursor.close()
    conn.close()
    return cards

def delete_card(card_id, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM vocab_cards WHERE id=%s AND user_id=%s",
            (card_id, user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        cursor.close()
        conn.close()
        return False, str(e)
