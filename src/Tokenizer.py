from sudachipy import tokenizer

import Constants
import Deinflect
from Grammar import Grammar, is_small_number, is_day_or_month
from Numbers import number_japanese_writing
import Dictionary


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
    def __init__(self, word, grammar=Grammar.UNKNOWN, root="", char_indices=(0,0), endings=None):
        self.word = word
        self.grammar = grammar
        if root == "":
            self.root = word
        else:
            self.root = root
        self.char_indices = char_indices
        self.endings = endings

    def __str__(self):
        return "(" + self.word + " | " + self.grammar.value + " | " + self.root + ")"

    def __repr__(self):
        return "(" + self.word + " | " + self.grammar.value + " | " + self.root + ")"


def tokenize_sudachi(text):
    mode = tokenizer.Tokenizer.SplitMode.C
    return [Token(m.surface(),
                  _make_grammar(m.part_of_speech()),
                  m.dictionary_form(),
                  (m.begin(), m.end()))
            for m in Constants.tokenizer.tokenize(text, mode)]


def merge_endings(tokens):
    i = 0
    merged = []
    while i < len(tokens):
        current = tokens[i]
        current_word = current.word
        current_grammar = current.grammar
        current_indices = current.char_indices
        if _conjugates(current) and i+1 < len(tokens):
            ending = ""
            ending_final = ""
            root = ""
            start = tokens[i + 1].char_indices[0]
            end = tokens[i + 1].char_indices[1]
            deinflict_reasons = []
            last_match = i
            original_token = tokens[i].word

            # current is an inflection itself
            deinflict = Deinflect.get_ending(original_token, original_token)
            if deinflict is not None:
                root_len = len(deinflict.root)
                start = current_indices[0] + root_len
                end = current_indices[1]
                current_indices = (current_indices[0],start)
                current_word = current.word[:root_len]
                root = deinflict.word
                ending_final = current.word[root_len:]
                deinflict_reasons = deinflict.reasons[0]

            while i + 1 < len(tokens):
                next_ = tokens[i + 1]
                if _might_be_ending(next_):
                    combination = current.word + ending + next_.word
                    deinflict = Deinflect.get_ending(combination, original_token)
                    if deinflict is not None:
                        current_word = current.word
                        current_indices = current_indices

                        end = next_.char_indices[1]
                        root = deinflict.word
                        deinflict_reasons = deinflict.reasons[0]
                        last_match = i
                        ending_final = ending + next_.word
                else:
                    break
                i += 1
                ending += next_.word
            if root != "":
                merged.append(Token(current_word, current_grammar, root, current_indices))  # word that is conjugated
                merged.append(Token(ending_final, Grammar.MERGED, char_indices=(start, end), endings=deinflict_reasons))  # ending to that word
                i = last_match + 2
            else:
                merged.append(_make_token_root(current))
                i = last_match + 1
            continue

        merged.append(_make_token_root(current))
        i += 1

    return merged

def _make_token_root(original):
    return Token(original.word, original.grammar, original.word, original.char_indices)

def _conjugates(current):
    return current.grammar == Grammar.VERB or current.grammar == Grammar.I_ADJECTIVE or current.grammar == Grammar.AUX_VERB

def _might_be_ending(token):
    return token.grammar == Grammar.PARTICLE or \
           token.grammar == Grammar.AUX_VERB or True


def _merge_words_using_dictionary(tokens):
    merged = []
    i = 0
    while i+1 < len(tokens):
        current = tokens[i].word
        next_ = tokens[i+1].word
        combination = current + next_
        combination = normalize_numbers(combination)
        dict_get = Dictionary.match(Token(combination), match_pos=False)
        if dict_get is not None and should_merge(current,next_, dict_get):
            start = tokens[i].char_indices[0]
            end = tokens[i+1].char_indices[1]
            merged.append(Token(dict_get[0].writings[0], dict_get[0].pos[0], dict_get[0].writings[0], (start, end)))
            if i+2 < len(tokens):
                i += 1
        else:
            merged.append(tokens[i])

        i += 1

    merged.append(tokens[i])
    return merged


def should_merge(current, next_, entry):
    if is_small_number(current) and is_day_or_month(next_):
        return True
    else:  # these tags are accepted since they have a low chance of producing an incorrect result
        return (entry[0].pos[0] == Grammar.NOUN or entry[0].pos[0] == Grammar.PRONOUN) and entry[0].writings[0] == current+next_


def normalize_numbers(string):
    return "".join([number_japanese_writing(c) for c in string])


def _is_ending(token):
    return (token.grammar == Grammar.AUX_VERB or token.word == "て" or token.word == "で" or token.word == "い" or token.word == "いる"
            or token.word == "な" or token.root == "しまう" or token.word == "そう" or token.word == "ば" or token.word == "なかっ") and token.word != "なら" and token.word != "だ"


def get_tokens(text: str):
    if text == "":
        print("Empty string passed to get_tokens")
        return []
    tokens = tokenize_sudachi(text)
    tokens = merge_endings(tokens)
    tokens = _merge_words_using_dictionary(tokens)
    return tokens
