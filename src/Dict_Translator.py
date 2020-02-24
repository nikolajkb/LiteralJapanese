from Grammar import Grammar, Ending, endings
from XmlReader import XmlReader
import Word

jp = 0
en = 1


def translate(tokens):
    translations = []

    for token in tokens:
        jp = token.word

        if is_ending(token):
            translation = translate_ending(token)
            translations.append((jp, translation))
            continue

        translation = match_special(jp)
        if translation:
            translations.append((jp, translation))
            continue

        translation = get_translation_from_dictionary(token.root)
        translations.append((jp, translation))

    return translations


def get_translation_from_dictionary(word):
    dictionary = XmlReader().get_dict()
    translations = dictionary.get(word)
    if translations:
        return translations[0].meanings[0]
    else:
        return "ERROR"


def is_ending(token):
    return token.grammar == Grammar.MERGED


def translate_ending(token):
    ending: str = token.word
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
        "が": "<ga>",
        "に": "<ni>",
        "で": "<de>",
        "の": "<no>",
        "は": "<wa>",
        "と": "<to>",
        "も": "<mo>",
        "ので": "so",
        "か": "?",
        "て": "<te>",
        "。": ".",
        "、": ",",
        "「": "\"",
        "」": "\"",
        "～": "-",
        "･･･": "...",
    }.get(token, None)
