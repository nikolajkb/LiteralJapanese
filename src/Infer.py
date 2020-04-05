import Dictionary
import Translator
import nltk
from Grammar import Grammar


# args are tokenized japanese and un-tokenized english
def infer(source,target):
    target = [t for t in nltk.tokenize.word_tokenize(target)]
    target = merge_s(target)
    original = target.copy()
    inferred_translations = []
    for token in source:
        inferred_translation = ""

        translations = get_all_meanings(token)

        for translation in translations:
            if token.grammar == Grammar.PARTICLE:
                small_distance = noun_distance_is_small(source, original, token, translation)
                if small_distance:
                    inferred_translation = translation
                    target.remove(translation)
                break

            if translation in target:
                inferred_translation = translation
                target.remove(translation)
                break

        if inferred_translation != "":
            inferred_translations.append(inferred_translation)
        else:
            inferred_translations.append(None)
    return inferred_translations


def get_all_meanings(token):
    entries = Dictionary.match(token)
    proper_nouns = Dictionary.get_proper_noun(token.word)
    if entries is None and proper_nouns is None:
        return []
    if proper_nouns is None:
        proper_nouns = []
    if entries is None:
        entries = []
    translations = []
    for entry in entries:
        translations.extend(entry.meanings)
    for entry in proper_nouns:
        translations.extend(entry.meanings)
    translations = [Translator.clean_word(t).strip() for t in translations]
    return translations


def noun_distance_is_small(jp_tokens, en_tokens, jp, en):
    if en not in en_tokens:
        return False
    last_jp_noun = find_last_jp_noun(jp_tokens,jp)
    noun_meanings = get_all_meanings(last_jp_noun)
    distance = en_distance_to_noun(noun_meanings,en,en_tokens)
    return distance < 3


def en_distance_to_noun(noun_meanings, en, en_tokens):
    index = None
    for meaning in noun_meanings:
        try:
            index = en_tokens.index(meaning)
        except ValueError:
            pass
    if index is None:
        return 999

    i = 0
    searching = True
    no_left = False
    no_right = False
    while searching:
        i += 1
        try:
            word = en_tokens[index+i]
            if word == en:
                return i
        except IndexError:
            no_right = True
        try:
            word = en_tokens[index-i]
            if word == en:
                return i
        except IndexError:
            no_left = True

        searching = not (no_left and no_right)

    return 999


# Japanese nouns always come before the particle that modifies them
def find_last_jp_noun(jp_tokens, jp):
    index = jp_tokens.index(jp)
    searching = True
    i = 0
    while searching:
        i += 1
        try:
            token = jp_tokens[index-i]
            if token.grammar == Grammar.NOUN:
                return token
        except IndexError:
            return None


def merge_s(tokens):
    i = 0
    for token in tokens:
        if token == "'" or token == "’" and tokens[i+1] == "s":
            return merge_s(tokens[:i] + ["'s"] + tokens[i+2:])
        i += 1
    return tokens
