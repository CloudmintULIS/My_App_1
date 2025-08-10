import psycopg2.extras
from models.db import get_db_connection

def get_vocab_cards(username):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        cursor.close()
        conn.close()
        return []

    user_id = user['id']
    cursor.execute(
        "SELECT word, image_path FROM vocab_cards WHERE user_id = %s ORDER BY timestamp DESC",
        (user_id,)
    )
    cards = cursor.fetchall()
    cursor.close()
    conn.close()
    return cards
