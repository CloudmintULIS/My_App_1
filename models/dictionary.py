# models/word_info_model.py
import psycopg2
from models.db_init import get_db_connection

def save_word_info(word, phonetic, audio, definition, example):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO word_info (word, phonetic, audio, definition, example)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (word) DO UPDATE
        SET phonetic = EXCLUDED.phonetic,
            audio = EXCLUDED.audio,
            definition = EXCLUDED.definition,
            example = EXCLUDED.example
        RETURNING id;
    """, (word, phonetic, audio, definition, example))
    word_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return word_id

def get_word_info_from_db(word):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT word, phonetic, audio, definition, example FROM word_info WHERE word=%s;", (word,))
    row = cur.fetchone()
    cur.close()
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
