from Grammar import Grammar, Ending, endings, is_hiragana
from XmlReader import XmlReader
import re

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

        translation = get_translation_from_dictionary(token)
        translations.append((jp, translation))

    return translations


def get_translation_from_dictionary(token):
    xml_reader = XmlReader().get_dict()
    dictionary = xml_reader.dictionary
    translations = dictionary.get(token.root)
    if translations:
        # if word is only kana, find definition that is usually written in kana
        if is_hiragana(token.word):
            kana_match = [t for t in translations if Grammar.USUALLY_KANA in t.misc]
            if kana_match:
                translations = kana_match

        # attempt to match pos
        pos_match = [t for t in translations if token.grammar in t.pos]
        if pos_match:
            translations = pos_match

        translation = translations[0].meanings[0]

        translation = clean_word(translation)
        return translation
    else:
        pn_dictionary = xml_reader.pn_dictionary
        translations = pn_dictionary.get(token.root)
        if translations:
            return translations[0].meanings[0]
        else:
            return "OOV"


def clean_word(word):
    word = re.sub(" ?\(.*\)", "", word)
    word = re.sub("to ", "", word)
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
        "?": "?"

    }.get(token, None)
