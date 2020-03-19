from enum import Enum
import re


# marked with * are my own definitions that I was not able to confirm
class Grammar(Enum):
    VERB = "verb"
    NOUN = "noun"
    MOD_NOUN = "*noun that modifies another noun"
    PARTICLE = "particle"
    PARTICLE_NO = "the no particle"
    PARTICLE_CONJ = "conjugating particle"
    PARTICLE_QUOTE = "quoting particle"
    DETERMINER = "determiner"
    NA_ADJECTIVE = "na adjective"
    I_ADJECTIVE = "i adjective"
    AUX_VERB = "auxiliary verb"
    ENDING = "word ending"
    PROPER_NOUN = "proper noun"
    SYMBOL = "symbol"
    OOV = "out of vocabulary"
    BLANK = "blank"
    SUFFIX = "suffix"
    PRE_NOUN = "pre-noun adjectival"
    INTERJECTION = "interjection"
    PREFIX = "prefix"
    SUB_SYMBOL = "supplementary symbol"
    CONJUNCTION = "conjunction"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    ERROR = "error"
    URL = "url"
    ENGLISH = "english word"
    CHINESE = "chinese writing"
    NUMBER = "number"
    UNKNOWN = "unknown word"
    COUNTER = "counter"
    HESITATE = "???"  # todo find out what this means
    ROMAJI = "transliteration of Japanese into the Latin alphabet"
    USUALLY_KANA = "usually written using only kana"
    USUALLY_KANJI = "usually written using kanji"
    MERGED = "ending of word"
    NOT_IN_SWITCH = "did not match switch case"


class Ending(Enum):
    NEGATIVE = "negative"
    POLITE = "polite"
    PAST = "past"
    TE_FORM = "te"
    CAN_DO = "can"
    PROGRESSIVE = "ongoing"
    POTENTIAL = "potential"
    PASSIVE = "passive"
    POT_PAS = "potential or passive"
    CAUSATIVE = "causative"
    IMPERATIVE = "imperative"
    UNINTENTIONAL = "unintentional"
    VOLITIONAL = "volitional"
    SEEMS = "seems"
    WANT = "want"
    IF = "if"
    TARA = "when"
    REQUEST = "please"
    UNKNOWN = "unknown"
    IGNORE = ""


endings = [("ま", [Ending.POLITE]),("せん", [Ending.NEGATIVE]),("た", [Ending.PAST]),
           ("ない", [Ending.NEGATIVE]),("な", [Ending.NEGATIVE]),("かった", [Ending.PAST]),
           ("て", [Ending.TE_FORM]),("られ", [Ending.POT_PAS]),("させ", [Ending.CAUSATIVE]),
           ("ろ", [Ending.IMPERATIVE]),("るな", [Ending.IMPERATIVE, Ending.NEGATIVE]),
           ("てい", [Ending.PROGRESSIVE]),("しま", [Ending.UNINTENTIONAL]),("じゃ", [Ending.UNINTENTIONAL]),
           ("ちゃ", [Ending.UNINTENTIONAL]),("させられ", [Ending.CAUSATIVE, Ending.PASSIVE]),
           ("たい", [Ending.WANT]),("たい", [Ending.WANT]),("てる", [Ending.PROGRESSIVE]),
           ("きゃ", [Ending.IF]),("ば", [Ending.IF]), ("ており",[Ending.PROGRESSIVE]),
           ("なさい",[Ending.REQUEST]), ("で", [Ending.TE_FORM]),
           ("そう", [Ending.SEEMS]), ("たら", [Ending.TARA]), ("れ", [Ending.PASSIVE]),
           ("でした", [Ending.PAST]), ("しょう", [Ending.VOLITIONAL]), ("でいる",[Ending.PROGRESSIVE]),
           ("てます",[Ending.PROGRESSIVE, Ending.POLITE]),("たく",[Ending.WANT])]


def is_hiragana(s):
    kana = "あいうえおかきくけこがぎぐげごさしすせそざじずぜぞたちつてとだぢづでどなにぬねのはひふへほばびぶべぼぱぴぷぺぽまみむめもやゆよらりるれろわゐゑをんっゃゅょぃーゔ"
    return check_alphabet(s, kana)


def is_katakana(s):
    kana = "アイウエオカキクケコガギグゲゴサシスセソザジズゼゾタチツテトダヂヅデドナニヌネノハヒフヘホバビブベボパピプペポマミムメモヤユヨラリルレロワヰヱヲンッャュョィーヴ"
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


def is_english(s: str):
    match = re.match("^[a-zA-Z0-9.,]*$", s)
    return match is not None
