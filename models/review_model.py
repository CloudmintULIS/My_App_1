from models.db import get_db_connection

def get_vocab_cards_by_user(user_id):
    """Lấy tất cả flashcards của user, kèm thông tin từ word_info nếu có"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT vc.id, vc.image_path, vc.word, vc.timestamp,
               wi.phonetic, wi.audio, wi.definition, wi.example
        FROM vocab_cards vc
        LEFT JOIN word_info wi ON vc.word = wi.word
        WHERE vc.user_id = %s
        ORDER BY vc.timestamp DESC
    """, (user_id,))

    cards = []
    for row in cursor.fetchall():
        cards.append({
            "id": row[0],
            "image_path": row[1],
            "word": row[2],
            "timestamp": row[3].strftime("%d/%m/%Y %H:%M"),
            "phonetic": row[4],
            "audio": row[5],
            "definition": row[6],
            "example": row[7]
        })

    cursor.close()
    conn.close()
    return cards


def delete_card(card_id, user_id):
    """Xóa flashcard theo card_id của user hiện tại"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM vocab_cards
            WHERE id = %s AND user_id = %s
        """, (card_id, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Exception as e:
        return False, str(e)
