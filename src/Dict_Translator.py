from XmlReader import XmlReader
import Word


def translate(tokens):
    dicti = XmlReader().get_dict()
    translation = []
    for token in tokens:
        jp = token.word
        special = match_special(jp)
        if special:
            translation.append((jp, special))
        else:
            eng = dicti.get(token.root)
            if eng is None:
                eng = Word.make_empty()
                eng.meanings.append("ERROR")
            translation.append((jp, eng.meanings[0]))

    return translation


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
