def count_number_of_spaces(text: str) -> int:
    """Подсчет колличества пробелов в строке"""

    space_count = 0

    for char in text:
        if char.isspace():
            space_count += 1

    return space_count

def extract_words(text: str) -> list:
    """Извлечение слов из строки"""

    text = text.lower()
    text = text.replace(',', ' ').replace('.', ' ')

    return text.split()

def count_words_shorter_than(words: list, max_length: int = 5) -> int:
    """Подсчет количества слов из списка, длинна которых меньше чем заданная"""

    count = 0

    for word in words:
        if len(word) < max_length:
            count += 1

    return count

def find_shortest_word_ending_with(words: list, char: str = 'd') -> str:
    """Поиск наименьшего слова, которое заканчивается на определенных символ"""

    shortest_word = None

    for word in words:
        if word.endswith(char):
            if shortest_word is None or len(word) < len(shortest_word):
                shortest_word = word

    return shortest_word

def sort_words_by_length_desc(words: list) -> list:
    """Сортировка слов в списке по убыванию"""

    return sorted(words, key=len, reverse=True)
