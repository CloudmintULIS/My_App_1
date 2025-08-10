import psycopg2
import psycopg2.extras
import os
from urllib.parse import urlparse

def get_db_connection():
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise Exception("Bạn cần set biến môi trường DATABASE_URL trước khi chạy!")

    result = urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        dbname=result.path[1:],  # bỏ dấu '/'
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )
    return conn


def save_vocab_card(username: str, image_path: str, word: str):
    conn = get_db_connection()
    # Sử dụng RealDictCursor để fetch ra dict thay vì tuple
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result is None:
        print(f"❌ Không tìm thấy user: {username}")
        cursor.close()
        conn.close()
        return

    user_id = result["id"]

    cursor.execute(
        "INSERT INTO vocab_cards (user_id, image_path, word) VALUES (%s, %s, %s)",
        (user_id, image_path, word)
    )

    conn.commit()
    cursor.close()
    conn.close()


def get_vocab_cards(username: str):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result is None:
        print(f"❌ Không tìm thấy user: {username}")
        cursor.close()
        conn.close()
        return []

    user_id = result["id"]

    cursor.execute(
        "SELECT word, image_path FROM vocab_cards WHERE user_id = %s", (user_id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [{"word": row["word"], "image_path": row["image_path"]} for row in rows]


def get_vocab_cards_by_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute(
        'SELECT * FROM vocab_cards WHERE user_id = %s ORDER BY timestamp DESC',
        (user_id,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return rows
