# services/translate_service.py
from deep_translator import GoogleTranslator

def translate_text(text: str, src: str = "en", dest: str = "vi") -> str:
    try:
        return GoogleTranslator(source=src, target=dest).translate(text)
    except Exception as e:
        print("❌ Translate error:", e)
        return None
