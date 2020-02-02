from enum import Enum


class Ending(Enum):
    NEGATIVE = "not"
    POLITE = "pol"
    PAST = "past"
    TE_FORM = "te"
    CAN_DO = "can"
    PROGRESSIVE = "ongoing"
    UNKNOWN = "unknown"
    IGNORE = ""


def _make_grammar(token):
    return {
        "ま": Ending.POLITE,
        "せんでし": Ending.NEGATIVE,
        "た": Ending.PAST,
        "ない": Ending.NEGATIVE,
        "なかっ": Ending.NEGATIVE

    }.get(token, Ending.UNKNOWN)


def _make_grammar_2(token):
    return {
        "ませ": Ending.POLITE,
        "ん": Ending.NEGATIVE,
        "でし": Ending.PAST,
        "た": Ending.NEGATIVE,

    }.get(token, Ending.UNKNOWN)


def translate_ending(tokens):
    endings = []
    for token in tokens:
        endings.append(_make_grammar(token.word))

    print(endings)
    return endings
