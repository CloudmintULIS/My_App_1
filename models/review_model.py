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
