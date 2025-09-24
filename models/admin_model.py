from models.db import get_db_connection

# ===================== USERS =====================

def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, role FROM users ORDER BY id")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {"id": r[0], "username": r[1], "password": r[2], "role": r[3]}
        for r in rows
    ]


def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    return {"id": row[0], "username": row[1], "role": row[2]} if row else None


def add_user(username, password, role):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, password, role),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


def update_user(user_id, username, role):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username=%s, role=%s WHERE id=%s",
            (username, role, user_id),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


# ===================== VOCAB CARDS =====================

def get_all_vocab_cards():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.id, v.user_id, u.username, v.word, v.image_path, v.timestamp
        FROM vocab_cards v
        JOIN users u ON v.user_id = u.id
        ORDER BY v.id
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "id": r[0],
            "user_id": r[1],
            "username": r[2],
            "word": r[3],
            "image_path": r[4],
            "timestamp": r[5]
        }
        for r in rows
    ]



def get_vocab_by_id(vocab_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, word, image_path FROM vocab_cards WHERE id=%s", (vocab_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    return {"id": row[0], "user_id": row[1], "word": row[2], "image_path": row[3]} if row else None


def update_vocab(vocab_id, word, image_path):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE vocab_cards SET word=%s, image_path=%s WHERE id=%s",
            (word, image_path, vocab_id),
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


def delete_vocab(vocab_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vocab_cards WHERE id=%s", (vocab_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

# ===================== WORD INFO =====================

def get_all_word_info():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, word, phonetic, audio, definition, example
        FROM word_info
        ORDER BY id
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "id": r[0],
            "word": r[1],
            "phonetic": r[2],
            "audio": r[3],
            "definition": r[4],
            "example": r[5]
        }
        for r in rows
    ]


def get_word_info_by_id(word_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, word, phonetic, audio, definition, example
        FROM word_info WHERE id=%s
    """, (word_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return {
        "id": row[0], "word": row[1], "phonetic": row[2],
        "audio": row[3], "definition": row[4], "example": row[5]
    } if row else None


def add_word_info(word, phonetic, audio, definition, example):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO word_info (word, phonetic, audio, definition, example)
            VALUES (%s, %s, %s, %s, %s)
        """, (word, phonetic, audio, definition, example))
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


def update_word_info(word_id, word, phonetic, audio, definition, example):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE word_info
            SET word=%s, phonetic=%s, audio=%s, definition=%s, example=%s
            WHERE id=%s
        """, (word, phonetic, audio, definition, example, word_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)


def delete_word_info(word_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM word_info WHERE id=%s", (word_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

# ===================== STATISTICS =====================

def get_user_stats():
    conn = get_db_connection()
    cur = conn.cursor()

    # Đếm số lượng vocab của mỗi user
    cur.execute("""
        SELECT u.username,
               COUNT(v.id) AS vocab_count
        FROM users u
        LEFT JOIN vocab_cards v ON u.id = v.user_id
        GROUP BY u.username
        ORDER BY vocab_count DESC;
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {"username": row[0], "vocab_count": row[1]}
        for row in rows
    ]

