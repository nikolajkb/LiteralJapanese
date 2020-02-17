from Grammar import Grammar
from XmlReader import XmlReader
import Word


def translate(tokens):
    dicti = XmlReader().get_dict()
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

        translation = dicti.get(token.root)
        if translation:
            translations.append((jp, translation.meanings[0]))
            continue

        translation = Word.make_empty()
        translation.meanings.append("ERROR")

    return translations


def is_ending(token):
    return token.grammar == Grammar.MERGED


def translate_ending(token):
    ending: str = token.word
    matches = [s for s in endings if ending.startswith(s)]
    if len(matches) == 0:
        return "-ENDING NO FOUND"
    else:
        longest = max(matches, key=len)
        print(longest)


endings = ["d", "dd", "ddd"]


def match_special(token):
    return {
        "を": "<o>",
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
        "": "<>",
        "": "<>",
        "": "<>",
        "": "<>",
        "": "<>",
        "": "<>",
        "": "<>",
        "": "<>",
        "": "<>",
        "": "<>",
        "": "<>",
        "": "<>"
    }.get(token, None)
