import json
from pathlib import Path
from pymystem3 import Mystem
from nltk.corpus import stopwords

stop_words = stopwords.words('russian')

m = Mystem()


def remove_punctuation(sentence):
    """
    Removes punctuation
    """
    cleaned_sentense = ''
    for symbol in sentence:
        if symbol.isalnum() or symbol.isspace():
            cleaned_sentense += symbol
    return cleaned_sentense


def remove_stop_words_and_lemmatize(sentence):
    """
    Removes stopwords and lemmatize
    """
    tokens = " ".join([token for token in sentence.split() if token not in stop_words])
    lemmas = m.lemmatize(tokens)
    return "".join(lemmas).strip()


def preprocess(data):
    """
    Makes basic text preprocessing
    """
    phrases_groups = [subtopic['phrases'] for subtopic in data['subtopics']]
    lemmatized_phrases_groups = []
    for phrases_group in phrases_groups:
        lemmatized_phrases_group = [remove_stop_words_and_lemmatize(remove_punctuation(phrase)) for phrase in phrases_group]
        lemmatized_phrases_groups.append(lemmatized_phrases_group)
    return lemmatized_phrases_groups


def write_preprocessed(phrases_groups):
    """
    Writes preprocessed phrases to the particular file
    """
    with open('preprocessed_phrases.txt', 'w', encoding='utf-8') as file:
        for phrases_group in phrases_groups:
            for phrase in phrases_group:
                file.write(phrase)
                file.write('\n')
            file.write('\n')


def read_preprocessed(file_path):
    """
    Reads preprocessed phrases from the file
    """
    file_path = Path('preprocessed_phrases.txt')
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    text = text.split('\n\n')
    phrases_groups = [phrases_group.split('\n') for phrases_group in text]
    return phrases_groups


def find_keywords(phrases_groups):
    """
    Finds keywords in group of phrases from the particular subtitle
    """
    all_words = []
    for phrases_group in phrases_groups:
        tokens = []
        for phrase in phrases_group:
            tokens.extend(phrase.split())
        group_frequencies = {token: tokens.count(token) for token in tokens}
        highest_frequencies = sorted(group_frequencies.items(), key=lambda x: -x[1])[:3]
        keywords = [comb[0] for comb in highest_frequencies]
        all_words.append(keywords)
    return [words for words in all_words if words]


def write_keywords(keywords):
    """
    Writes extracted keywords to the particular file
    """
    with open('extracted_keywords.txt', 'w', encoding='utf-8') as file:
        for group in keywords:
            file.write(group[0] + ', ' + group[1] + ', ' + group[2])
            file.write('\n\n')


def read_keywords(file_path):
    """
    Reads keywords from the file
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().split('\n\n')
    keywords = [words.split() for words in text]
    return keywords


def find_words_in_lemmas_sequence(tokens, word):
    """
    As regular expressions do, finds the necessary word (keyword)
    in the preprocessed sentence (sequence of tokens)

    Returns 1 if the word is in the sentence and 0 if is not
    """
    result = tokens.count(word)
    if result == 0:
        return 0
    else:
        return 1
