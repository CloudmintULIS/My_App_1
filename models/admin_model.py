import psycopg2.extras
from models.db import get_db_connection

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def add_user(username, password, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, password, role)
        )
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def update_user(user_id, username, password, role):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE users SET username = %s, password = %s, role = %s WHERE id = %s",
            (username, password, role, user_id)
        )
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def get_all_vocab_cards():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
        SELECT vocab_cards.id, users.username, vocab_cards.word, vocab_cards.image_path, vocab_cards.timestamp
        FROM vocab_cards
        JOIN users ON vocab_cards.user_id = users.id
        ORDER BY vocab_cards.timestamp DESC
    """)
    vocab_cards = cursor.fetchall()
    cursor.close()
    conn.close()
    return vocab_cards

def get_vocab_by_id(vocab_id):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM vocab_cards WHERE id = %s", (vocab_id,))
    vocab = cursor.fetchone()
    cursor.close()
    conn.close()
    return vocab

def update_vocab(vocab_id, word, image_path):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE vocab_cards SET word = %s, image_path = %s WHERE id = %s",
            (word, image_path, vocab_id)
        )
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()

def delete_vocab(vocab_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM vocab_cards WHERE id = %s", (vocab_id,))
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close()
        conn.close()
