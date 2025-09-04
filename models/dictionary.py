# models/word_info_model.py
import psycopg2
from models.db_init import get_db_connection

def save_word_info(word, phonetic, audio, definition, example, cursor=None):
    """
    Lưu hoặc cập nhật word_info. Nếu cursor được cung cấp thì dùng, không thì tự tạo.
    """
    own_conn = False
    if cursor is None:
        conn = get_db_connection()
        cursor = conn.cursor()
        own_conn = True

    cursor.execute("""
        INSERT INTO word_info (word, phonetic, audio, definition, example)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (word) DO UPDATE
        SET phonetic = EXCLUDED.phonetic,
            audio = EXCLUDED.audio,
            definition = EXCLUDED.definition,
            example = EXCLUDED.example
        RETURNING id;
    """, (word, phonetic, audio, definition, example))

    word_id = cursor.fetchone()[0]

    if own_conn:
        conn.commit()
        cursor.close()
        conn.close()

    return word_id


def get_word_info_from_db(word, cursor=None):
    """
    Lấy thông tin word_info từ DB. Nếu cursor được cung cấp thì dùng, không thì tự tạo.
    """
    own_conn = False
    if cursor is None:
        conn = get_db_connection()
        cursor = conn.cursor()
        own_conn = True

    cursor.execute("SELECT word, phonetic, audio, definition, example FROM word_info WHERE word=%s;", (word,))
    row = cursor.fetchone()

    if own_conn:
        cursor.close()
        conn.close()

    if row:
        return {
            "word": row[0],
            "phonetic": row[1],
            "audio": row[2],
            "definition": row[3],
            "example": row[4]
        }
    return None
