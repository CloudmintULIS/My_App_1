import random

def generate_quiz(cards):
    unique_words = list({c['word'] for c in cards})
    if len(unique_words) < 4:
        return None, "Bạn cần ít nhất 4 từ vựng khác nhau để chơi quiz."

    correct_card = random.choice(cards)
    correct_word = correct_card['word']
    image_path = correct_card['image_path']

    wrong_pool = [w for w in unique_words if w != correct_word]
    if len(wrong_pool) < 3:
        return None, "Không đủ từ vựng sai để tạo quiz."

    wrong_choices = random.sample(wrong_pool, 3)

    all_choices = wrong_choices + [correct_word]
    random.shuffle(all_choices)

    return {
        "image_path": image_path,
        "choices": all_choices,
        "correct_word": correct_word
    }, None
