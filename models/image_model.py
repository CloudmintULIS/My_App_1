import psycopg2.extras
from models.db import get_db_connection

def save_vocab_card(username: str, image_path: str, word: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user is None:
        cursor.close()
        conn.close()
        return False, "User not found"

    user_id = user["id"]
    cursor.execute(
        "INSERT INTO vocab_cards (user_id, image_path, word) VALUES (%s, %s, %s)",
        (user_id, image_path, word)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True, None
