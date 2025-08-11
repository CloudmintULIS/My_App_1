import psycopg2.extras
from models.db import get_db_connection

def get_next_vocab_card_id() -> int:
    """
    Lấy ID kế tiếp từ sequence vocab_cards_id_seq
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nextval('vocab_cards_id_seq')")
    image_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return image_id

def save_vocab_card(username, image_url, label, vocab_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO vocab_cards (id, user_id, image_path, word) VALUES (%s, %s, %s, %s)",
            (vocab_id, user_id, image_url, label)
        )
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

