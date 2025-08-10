import random

def generate_quiz(cards):
    if len(cards) < 4:
        return None, "Bạn cần ít nhất 4 từ vựng để chơi quiz."

    correct_card = random.choice(cards)
    correct_word = correct_card['word']
    image_path = correct_card['image_path']

    wrong_choices = random.sample(
        [c['word'] for c in cards if c['word'] != correct_word], 3
    )

    all_choices = wrong_choices + [correct_word]
    random.shuffle(all_choices)

    return {
        "image_path": image_path,
        "choices": all_choices,
        "correct_word": correct_word
    }, None
