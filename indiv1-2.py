from itertools import permutations

def apply_permutation(block, perm):
    # Применяем перестановку только если блок заполнен
    if len(block) != len(perm):
        return block  # Возвращаем блок без изменений, если он неполный
    return ''.join(block[i] for i in perm)

# Задайте текст и длину блока
text = "а есОн порлав емти тхиняи ебо олнвзми суо емлитрнам а я лгена всаз, иои"
block_size = 6

# Разделите текст на блоки
blocks = [text[i:i + block_size] for i in range(0, len(text), block_size)]

# Загрузите список слов
with open('russian_words.txt', 'r', encoding='utf-8') as f:
    valid_words = set(word.strip().lower() for word in f)

found_words = False  # Флаг для проверки, найдены ли слова

# Перебор всех перестановок
all_permutations = list(permutations(range(block_size)))

for perm in all_permutations:
    decrypted_blocks = [apply_permutation(block, perm) for block in blocks]
    decrypted_text = ''.join(decrypted_blocks).replace('\n', '').replace('\t', '').strip()  # Убираем лишние символы

    # Проверка на наличие слов в расшифрованном тексте
    if any(word in decrypted_text.lower() for word in valid_words):
        print(f"Decrypted text: {decrypted_text}")
        found_words = True

if not found_words:
    print("No meaningful words found in the decrypted text.")
