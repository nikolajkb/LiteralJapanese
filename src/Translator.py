import Dictionary
import Infer
import Numbers
from Grammar import Grammar, is_english, is_katakana, is_number
import re
import Katakana

jp = 0
en = 1


def translate(tokens, translation=None):
    translations = []

    inferred_meanings = None
    if translation is not None:
        inferred_meanings =None# Infer.infer(tokens,translation)

    i = -1
    for token in tokens:
        i += 1
        jp = token.word
        is_last = i == len(tokens) - 1

        if is_ending(token):
            translation = translate_ending(token)
            translations.append((jp, translation))
            continue

        if inferred_meanings is not None:
            translation = inferred_meanings.get(token.word)
            if translation is not None:
                translations.append((jp, translation))
                continue

        translation = match_special(jp,is_last)
        if translation:
            translations.append((jp, translation))
            continue

        translation = get_translation_from_dictionary(token)
        if translation:
            translations.append((jp, translation))
            continue

        if is_katakana(jp):
            translations.append((jp,Katakana.translate(jp)))
            continue

        if is_english(jp):
            translations.append((jp, jp))
            continue

        if is_number(jp):
            translations.append((jp,Numbers.convert(jp)))
            continue

        translations.append((jp, "OOV"))

    return translations


def get_translation_from_dictionary(token):
    translations = Dictionary.match(token)
    if translations:
        translation = clean_word(translations[0].meanings[0])
        return translation
    else:
        translations = Dictionary.get_proper_noun(token.root)
        if translations:
            return translations[0].meanings[0]
        else:
            return None


# the point of this method is to make the word look more
# like a word in a sentence and less like a dictionary entry
def clean_word(word):
    word = re.sub("\(.*\) ?", "", word)    # remove anything in parentheses
    word = re.sub("^to (?=.+)", "", word)  # remove to in "to play" etc.
    word = re.sub("^be (?=.+)","",word)    # remove be in "be happy" etc.
    word = word.strip()
    return word


def is_ending(token):
    return token.grammar == Grammar.MERGED


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
        "氏": "shi"
    }

    # se = sentence ending
    ends = {
        "な": "musing (se)",
        "の": "explain (se)",  # the only ambiguous end, 'no' might be used as a question marker or as the 'explainer'-no. logic for translation: Explain could mean explain to me or I'm explaining to you
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
