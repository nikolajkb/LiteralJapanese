from sudachipy import tokenizer
from sudachipy import dictionary
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
    MERGED = "verb with endings"
    NOT_IN_SWITCH = "did not match switch case"


def _make_grammar(tag):
    return {
        "名詞": Grammar.NOUN,
        "助詞": Grammar.PARTICLE,
        "形状詞": Grammar.NA_ADJECTIVE,
        "助動詞": Grammar.AUX_VERB,
        "補助記号": Grammar.SUB_SYMBOL,
        "oov": Grammar.OOV,
        "空白": Grammar.BLANK,
        "接尾辞": Grammar.SUFFIX,
        "動詞": Grammar.VERB,
        "連体詞": Grammar.PRE_NOUN,
        "形容詞": Grammar.I_ADJECTIVE,
        "感動詞": Grammar.INTERJECTION,
        "接頭辞": Grammar.PREFIX,
        "記号": Grammar.SYMBOL,
        "接続詞": Grammar.CONJUNCTION,
        "副詞": Grammar.ADVERB,
        "代名詞": Grammar.PRONOUN,
        "web誤脱": Grammar.ERROR,
        "URL": Grammar.URL,
        "英単語": Grammar.ENGLISH,
        "漢文": Grammar.CHINESE,
        "未知語": Grammar.UNKNOWN,
        "言いよどみ": Grammar.HESITATE,
        "ローマ字文": Grammar.ROMAJI
    }.get(tag[0], Grammar.NOT_IN_SWITCH)


class Token:
    def __init__(self, word, grammar, root):
        self.word = word
        self.grammar = grammar
        self.root = root

    def __str__(self):
        return "(" + self.word + " | " + self.grammar.value + ")"

    def __repr__(self):
        return "(" + self.word + " | " + self.grammar.value + " | " + self.root + ")"


def _tokenize(text):
    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.C

    return [Token(m.surface(),
                  _make_grammar(m.part_of_speech()),
                  m.dictionary_form())
            for m in tokenizer_obj.tokenize(text, mode)]


def _merge_verb_endings(tokens):
    merged = []
    for i in range(len(tokens)):
        if tokens[i].grammar == Grammar.VERB:
            verb_with_endings = tokens[i].word
            i += 1
            while i < len(tokens) and tokens[i].grammar == Grammar.AUX_VERB:
                verb_with_endings += tokens[i].word
                i += 1
            merged.append(Token(verb_with_endings, Grammar.MERGED))
        elif tokens[i].grammar != Grammar.AUX_VERB:
            merged.append(tokens[i])

    return merged


def get_tokens(text):
    print(text)
    tokens = _tokenize(text)
    # tokens = _merge_verb_endings(tokens)
    print(tokens)
    return tokens
