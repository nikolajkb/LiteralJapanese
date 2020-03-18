import Dictionary
import Infer
from Grammar import Grammar, endings, is_english
import re

jp = 0
en = 1


def translate(tokens, translation=None):
    translations = []

    inferred_meanings = None
    if translation is not None:
        inferred_meanings = None#Infer.infer(tokens,translation)

    i = -1
    for token in tokens:
        i += 1
        jp = token.word

        if is_ending(token):
            translation = translate_ending(token)
            translations.append((jp, translation))
            continue

        if inferred_meanings is not None:
            translation = inferred_meanings.get(token.word)
            if translation is not None:
                translations.append((jp, translation))
                continue

        translation = match_special(jp)
        if translation:
            translations.append((jp, translation))
            continue

        translation = get_translation_from_dictionary(token)
        if translation:
            translations.append((jp, translation))
            continue

        if is_english(jp):
            translations.append((jp, jp))
        else:
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
    word = re.sub(" ?\(.*\)", "", word)
    word = re.sub("^to ", "", word)
    word = re.sub("^be ","",word)
    return word


def is_ending(token):
    return token.grammar == Grammar.MERGED


def translate_ending(token):
    ending: str = token.word
    if ending == "な":  # not including this special case would make the algorithm more complicated
        return "-imperative-negative"
    ending_en = ""
    while ending:
        matches = [s for s in endings if ending.startswith(s[jp])]
        if len(matches) == 0:
            ending = ending[1:]
        else:
            longest = max(matches, key=lambda m: len(m[0]))
            for end in longest[en]:
                ending_en += "-" + end.value
            ending = ending[len(longest[jp]):]

    return ending_en


def match_special(token):
    return {
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
        "ので": "so", # todo this is not matched since it's two tokens
        "か": "?",
        "て": "<te>",
        "よ": ", you know?",
        "ね": ", right?",
        "。": ".",
        "、": ",",
        "「": "\"",
        "」": "\"",
        "～": "-",
        "･･･": "...",
        " ": " ",
        "？": "?",
        "?": "?",
        "・": " "

    }.get(token, None)
