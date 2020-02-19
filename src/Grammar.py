from enum import Enum


class Grammar(Enum):
    VERB = "verb"
    NOUN = "noun"
    PARTICLE = "particle"
    NA_ADJECTIVE = "na adjective"
    I_ADJECTIVE = "i adjective"
    AUX_VERB = "auxiliary verb"
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
    UNKNOWN = "unknown word"
    HESITATE = "???"  # todo find out what this means
    ROMAJI = "transliteration of Japanese into the Latin alphabet"
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
    WANT = "want"
    IF = "if"
    UNKNOWN = "unknown"
    IGNORE = ""


endings = [("ま", [Ending.POLITE]), ("せん", [Ending.NEGATIVE]), ("た", [Ending.PAST]),
           ("ない", [Ending.NEGATIVE]),("な", [Ending.NEGATIVE]), ("かった", [Ending.PAST]),
           ("て", [Ending.TE_FORM]), ("られ", [Ending.POT_PAS]), ("させ", [Ending.CAUSATIVE]),
           ("ろ", [Ending.IMPERATIVE]), ("るな", [Ending.IMPERATIVE, Ending.NEGATIVE]),
           ("てい", [Ending.PROGRESSIVE]),("しま", [Ending.UNINTENTIONAL]),("じゃ", [Ending.UNINTENTIONAL]),
           ("ちゃ", [Ending.UNINTENTIONAL]), ("させられ", [Ending.CAUSATIVE, Ending.PASSIVE]),
           ("たい", [Ending.WANT]), ("たい", [Ending.WANT])]
