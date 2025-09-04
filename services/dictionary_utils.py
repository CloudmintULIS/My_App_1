# services/dictionary_utils.py
import requests
from models.dictionary import save_word_info, get_word_info_from_db
from models.db import get_db_connection  # hàm cũ của bạn

def fetch_word_info(word, conn=None):
    """
    Tra từ và lưu vào DB.
    Nếu có conn từ ngoài thì dùng, nếu không thì tự tạo kết nối.
    """
    own_conn = False
    if conn is None:
        conn = get_db_connection()
        own_conn = True

    cursor = conn.cursor()

    # 1️⃣ Kiểm tra trong DB trước
    cached = get_word_info_from_db(word, cursor=cursor)  # cần sửa get_word_info_from_db nhận cursor
    if cached:
        if own_conn:
            cursor.close()
            conn.close()
        return cached

    # 2️⃣ Nếu chưa có thì gọi API
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()[0]
            phonetic = data.get("phonetic", "")
            audio = ""
            for p in data.get("phonetics", []):
                if p.get("audio"):
                    audio = p["audio"]
                    break
            meaning = data.get("meanings", [])
            definition = meaning[0]["definitions"][0]["definition"] if meaning else ""
            example = meaning[0]["definitions"][0].get("example", "") if meaning else ""

            # 3️⃣ Lưu vào DB (upsert)
            save_word_info(word, phonetic, audio, definition, example, cursor=cursor)

            conn.commit()

            if own_conn:
                cursor.close()
                conn.close()

            return {
                "word": word,
                "phonetic": phonetic,
                "audio": audio,
                "definition": definition,
                "example": example
            }
    except Exception as e:
        print("❌ Dictionary API error:", e)

    if own_conn:
        cursor.close()
        conn.close()

    return None
