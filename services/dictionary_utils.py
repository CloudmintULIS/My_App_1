# services/dictionary_utils.py
import requests
from models.dictionary import save_word_info, get_word_info_from_db

def fetch_word_info(word):
    # 1️⃣ Kiểm tra trong DB trước
    cached = get_word_info_from_db(word)
    if cached:
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
            save_word_info(word, phonetic, audio, definition, example)

            return {
                "word": word,
                "phonetic": phonetic,
                "audio": audio,
                "definition": definition,
                "example": example
            }
    except Exception as e:
        print("❌ Dictionary API error:", e)

    return None
def fill_missing_word_info(word):
    """
    Nếu từ trong DB thiếu phonetic/definition/example -> gọi API và update lại.
    """
    word_info = get_word_info_from_db(word)

    # Nếu chưa có trong DB → fetch mới luôn
    if not word_info:
        api_data = fetch_word_info(word)
        if api_data:
            save_word_info(
                api_data["word"],
                api_data["phonetic"],
                api_data["audio"],
                api_data["definition"],
                api_data["example"]
            )
            return api_data
        return None

    # Nếu có rồi nhưng thiếu thông tin → bổ sung
    if not word_info["phonetic"] or not word_info["definition"] or not word_info["example"]:
        api_data = fetch_word_info(word)
        if api_data:
            # update với dữ liệu mới (kể cả nếu cũ NULL)
            save_word_info(
                api_data["word"],
                api_data["phonetic"] or word_info["phonetic"],
                api_data["audio"] or word_info["audio"],
                api_data["definition"] or word_info["definition"],
                api_data["example"] or word_info["example"]
            )
            return api_data
    return word_info