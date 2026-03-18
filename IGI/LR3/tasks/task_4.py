from text_core.text_analyzer import (
extract_words,
count_words_shorter_than,
find_shortest_word_ending_with,
sort_words_by_length_desc
)

def execute():
    """Выполнение четвертого задания - ввод, обработка, вывод"""

    print("\nЗадание 4")

    source_text = ("So she was considering in her own mind, as well as she could, for the hot day made her feel "
                   "very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble "
                   "of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by "
                   "her.")

    words_list = extract_words(source_text)

    print("\n--- РЕЗУЛЬТАТЫ ---")

    short_words_count = count_words_shorter_than(words_list, 5)
    print(f"a) Слов короче 5 символов: {short_words_count}")

    shortest_d = find_shortest_word_ending_with(words_list, 'd')
    print(f"б) Самое короткое слово: {shortest_d}")

    sorted_words = sort_words_by_length_desc(words_list)
    print(f"в) Слова в порядке убывания: {sorted_words}")

    print("-" * 18)


