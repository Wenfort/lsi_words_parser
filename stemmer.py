import pymorphy2
import re


def _is_functional_part_of_speech(part_of_speech):
    if part_of_speech in ['PREP', 'CONJ', 'PRCL', 'INTJ']:
        return True

def _is_number(tag):
    if 'ЧИСЛО' in tag.cyr_repr:
        return True

def delete_punctuation_from_word(word):
    return re.sub(r'[^\w\s]', '', word)


def stem_text(words, is_punctuation_needed=True):
    """
    Стемироание - приведение слова к его изначальной форме. Например, слова "покупка" и "купить" будет приведены
    к слову "купить". Это очень полезно для оценки конкуренции по вхождению ключевых слов в заголовок страницы.
    Метод _is_functional_part_of_speech отсекает служебные части речи. Они не нужны.
    """
    morpher = pymorphy2.MorphAnalyzer()
    stemmed_text = []
    for word in words:

        if not is_punctuation_needed:
            word = delete_punctuation_from_word(word)

        stemed_word = morpher.parse(word)
        the_best_form_of_stemed_word = stemed_word[0]

        part_of_speech = str(the_best_form_of_stemed_word.tag.POS)


        if not _is_functional_part_of_speech(part_of_speech) and not _is_number(the_best_form_of_stemed_word.tag):
            final_word = the_best_form_of_stemed_word.normal_form
            stemmed_text.append(final_word)

    return stemmed_text
