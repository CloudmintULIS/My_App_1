from datetime import datetime

def prepare_cards_for_review(cards):
    prepared = []
    for card in cards:
        # xử lý timestamp
        ts = card.get("timestamp")
        if ts and isinstance(ts, datetime):
            ts = ts.strftime("%d/%m/%Y %H:%M")

        # Dùng trực tiếp dữ liệu từ DB, không gọi fill_missing_word_info
        prepared.append({
            "id": card.get("id"),
            "word": (card.get("word") or "").capitalize(),
            "phonetic": card.get("phonetic") or "",
            "definition": card.get("definition") or "",
            "example": card.get("example") or "",
            "image_path": card.get("image_path") or "",
            "timestamp": ts
        })
    return prepared
