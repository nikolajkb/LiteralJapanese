from XmlReader import XmlReader
import Word


def translate(tokens):
    dicti = XmlReader().get_dict()
    translations = []

    for token in tokens:
        jp = token.word

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
