from enum import Enum
import re


class Grammar(Enum):
    # POS
    VERB = "verb"
    NOUN = "noun"
    PARTICLE = "particle"
    NA_ADJECTIVE = "na adjective"
    I_ADJECTIVE = "i adjective"
    SYMBOL = "symbol"
    BLANK = "blank"
    SUFFIX = "suffix"
    PRE_NOUN = "pre-noun adjectival"
    INTERJECTION = "interjection"
    PREFIX = "prefix"
    SUB_SYMBOL = "supplementary symbol"
    CONJUNCTION = "conjunction"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    AUX_VERB = "auxiliary verb"

    # misc tags from dictionary
    USUALLY_KANA = "usually written using only kana"
    USUALLY_KANJI = "usually written using kanji"

    # tags used by system
    MERGED = "ending of word"
    NOT_IN_SWITCH = "did not match switch case"
    UNKNOWN = "grammar not known"


def is_hiragana(s):
    kana = "あいうえおかきくけこがぎぐげごさしすせそざじずぜぞたちつてとだぢづでどなにぬねのはひふへほばびぶべぼぱぴぷぺぽまみむめもやゆよらりるれろわゐゑをんっゃゅょぃーゔぇ"
    return check_alphabet(s, kana)


def is_katakana(s):
    kana = "アイウエオカキクケコガギグゲゴサシスセソザジズゼゾタチツテトダヂヅデドナニヌネノハヒフヘホバビブベボパピプペポマミムメモヤユヨラリルレロワヰヱヲンッャュョィーヴェ"
    return check_alphabet(s, kana)


def is_number(s):
    numbers = "1234567890１２３４５６７８９０〇一二三四五六七八十千万億兆京"
    return check_alphabet(s,numbers)


def is_small_number(s):
    numbers = "1234567890１２３４５６７８９０〇一二三四五六七八十"
    return check_alphabet(s,numbers)


def is_day_or_month(s):
    day_and_month = "日月"
    return check_alphabet(s,day_and_month)


def check_alphabet(s: str, kana):
    for c in list(s):
        if kana.find(c) == -1:
            return False
    return True


def is_english(s):
    return re.match("^[a-zA-Z0-9.,]*$", s) is not None


def is_english_words_no_symbols(s):
    return re.match("^[a-zA-Z0-9 ]*$", s) is not None


# what, who, when, where
def is_wh_question(word: str):
    questions = ["何","誰","いつ","どこ"]
    return True in [word.startswith(q) for q in questions]
