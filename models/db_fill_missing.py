# db_fill_missing.py
import psycopg2
import os
from dotenv import load_dotenv
from services.dictionary_utils import fetch_word_info

# 1️⃣ Load biến môi trường từ .env
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise Exception("Bạn cần set biến môi trường DATABASE_URL trong file .env!")

def fill_missing_word_info_from_vocab():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # 2️⃣ Lấy tất cả từ trong vocab_cards chưa có trong word_info
    cursor.execute('''
        SELECT DISTINCT vc.word
        FROM vocab_cards vc
        LEFT JOIN word_info wi ON vc.word = wi.word
        WHERE wi.word IS NULL
    ''')
    missing_words = [row[0] for row in cursor.fetchall()]
    print(f"Found {len(missing_words)} words missing info.")

    # 3️⃣ Lặp qua từng từ và điền info
    for word in missing_words:
        try:
            info = fetch_word_info(word, conn=conn)  # cần sửa fetch_word_info nhận conn từ ngoài
            if info:
                cursor.execute('''
                    INSERT INTO word_info (word, phonetic, audio, definition, example)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (word) DO NOTHING
                ''', (
                    word,
                    info.get('phonetic', ''),
                    info.get('audio', ''),
                    info.get('definition', ''),
                    info.get('example', '')
                ))
                print(f"✅ Filled info for word: {word}")
            else:
                print(f"⚠️ No info found for word: {word}")
        except Exception as e:
            print(f"❌ Error fetching info for {word}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Done filling missing word_info.")

if __name__ == "__main__":
    fill_missing_word_info_from_vocab()
