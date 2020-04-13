import Dictionary
import Infer
import Numbers
from Grammar import Grammar, is_english, is_katakana, is_number
import re
import Katakana


class Translation:
    def __init__(self,token, english):
        self.japanese = token.word  # this is technically redundant, but provides nicer access pattern
        self.english = english
        self.token = token


def translate(tokens, translation=None):
    translations = []
    dict_translations = []

    inferred_meanings = None
    if translation is not None:
        inferred_meanings = Infer.infer(tokens,translation)

    i = -1
    for token in tokens:
        i += 1
        jp = token.word
        last = i == len(tokens) - 1
        if not last:
            if is_sentence_ending_symbol(tokens[i+1].word):
                last = True

        if is_ending(token):
            translation = translate_ending(token)
            translations.append(Translation(token, translation))
            continue

        translation = match_special(jp,last)
        if translation:
            translations.append(Translation(token, translation))
            continue

        if inferred_meanings is not None:
            translation = inferred_meanings[i]
            if translation is not None:
                translations.append(Translation(token, translation))
                continue

        translation = get_translation_from_dictionary(token)
        if translation:
            dict_translations.append((token,translation))
            translations.append(None)
            continue

        if is_katakana(jp):
            translations.append(Translation(token,Katakana.translate(jp)))
            continue

        if is_english(jp):
            translations.append(Translation(token, jp))
            continue

        if is_number(jp):
            translations.append(Translation(token,Numbers.convert(jp)))
            continue

        translations.append(Translation(token, "OOV"))

    return translations


def get_translation_from_dictionary(token):
    translations = Dictionary.match(token)
    if translations:
        return [[clean_word(m) for m in translation.meanings] for translation in translations]
    else:
        translations = Dictionary.get_proper_noun(token.root)
        if translations:
            return translations[0].meanings[0]
        else:
            return None


def add_dict_translations(translations,dict_translations):
    for translation in translations:
        if translation is None:
            translation = dict_translations.pop(0)


# the point of this method is to make the word look more
# like a word in a sentence and less like a dictionary entry
def clean_word(word):
    word = remove_parentheses(word)        # remove anything in parentheses
    word = re.sub("^to (?=.+)", "", word)  # remove to in "to play" etc.
    word = re.sub("^be (?=.+)","",word)    # remove be in "be happy" etc.
    word = word.strip()
    return word


# regular expressions do not cut it here since parentheses may be nested
def remove_parentheses(word: str):
    start = None
    depth = 0
    i = 0
    for char in word:
        if char == "(":
            if depth == 0:
                start = i
            depth += 1
        elif char == ")":
            if depth == 1:
                removed = word[:start] + word[i+1:]
                return remove_parentheses(removed)  # this allows for multiple pairs of parentheses
            depth -= 1
        i += 1
    return word


def is_ending(token):
    return token.grammar == Grammar.MERGED


def is_sentence_ending_symbol(string):
    return string in ["。","か","ね","な", "だ","？","?", ".", "」"]


def translate_ending(token):
    ending = [r.value for r in token.endings]
    return "".join(ending)


def match_special(token, is_last):
    universal = {
        # particles
        "を": "<o>",
        "お": "pol-",
        "が": "<ga>",
        "に": "<ni>",
        "で": "<de>",
        "の": "<no>",
        "は": "<wa>",
        "と": "<to>",
        "も": "<mo>",
        "ん": "<no>",
        "な": "<na>",
        "か": "?",
        "て": "<te>",
        "や": "or",

        # symbols
        "。": ".",
        "、": ",",
        "「": "\"",
        "」": "\"",
        "～": "-",
        "･･･": "...",
        " ": " ",
        "？": "?",
        "?": "?",
        "・": " ",
        
        # name suffixes
        "さん": "san",
        "ちゃん": "chan",
        "さま": "sama",
        "様": "sama",
        "くん": "kun",
        "たん": "tan",
        "殿": "dono",
        "どの": "dono",
        "氏": "shi",
        
        # copula
        "だ": "is",
        "です": "is",
        "である": "is",
        "であります": "is",
        "でござる": "is",
        "で御座る": "is",
        "でご座る": "is",
        "でございます": "is",
        "っす": "is",
    }

    # se = sentence ending
    ends = {
        "な": "musing (se)",
        "の": "explain (se)",  # the only ambiguous end, 'no' might be used as a question marker or as the 'explainer'-no. logic for translation: Explain could mean explain to me or I'm explaining to you
        "ん": "explain (se)",  # short version of no
        "ぞ": "! (se)",
        "わ": "feminine (se)",  # not a formal definition, but is mostly used by women to make the sentence "softer"
        "かな": "i wonder (se)",
        "ぜ": "! (se)",
        "さ": "hey (se)",  # used when trying to get someones attention
        "よ": "you know? (se)",  # used to present new information
        "ね": "right? (se)",  # used to seek agreement
    }

    if is_last:
        return ends.get(token,universal.get(token,None))
    else:
        return universal.get(token,None)
