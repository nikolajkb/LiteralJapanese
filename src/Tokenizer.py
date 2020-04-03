from sudachipy import tokenizer

import Constants
import Deinflect
from Grammar import Grammar, is_small_number, is_day_or_month, is_wh_question
from Numbers import number_japanese_writing
import Dictionary


def _make_grammar(tag):
    return {
        "名詞": Grammar.NOUN,
        "助詞": Grammar.PARTICLE,
        "形状詞": Grammar.NA_ADJECTIVE,
        "助動詞": Grammar.AUX_VERB,
        "補助記号": Grammar.SUB_SYMBOL,
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
    }.get(tag[0], Grammar.NOT_IN_SWITCH)


class Token:
    def __init__(self, word="", grammar=Grammar.UNKNOWN, root="", char_indices=None, endings=None):
        if char_indices is None:
            char_indices = [-1, -1]
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
                  [m.begin(), m.end()])
            for m in Constants.tokenizer.tokenize(text, mode)]


def merge_endings(tokens):
    i = 0
    merged = []
    while i < len(tokens):
        current = tokens[i]
        conjugated_word = _copy_token(current)
        ending = Token()
        if _conjugates(current):

            # in case current is an inflection itself
            _split_conjugated_token(conjugated_word,ending,current)

            # add together all endings
            last_match = _add_endings(i,tokens,current,ending,conjugated_word)

            if ending.grammar == Grammar.MERGED:
                merged.append(conjugated_word)  # word that is conjugated

                ending.char_indices[0] = conjugated_word.char_indices[1]
                merged.append(ending)  # ending to that word
                i = last_match + 1
            else:  # no endings found
                merged.append(current)
                i = last_match + 1
            continue

        merged.append(current)
        i += 1

    return merged

# returns the index of the last token that contributed to a valid ending
def _add_endings(i,tokens,current,ending,conjugated_word):
    ending_to_test = ""
    last_match = i
    while i + 1 < len(tokens):
        next_ = tokens[i + 1]
        if _might_be_ending(next_):
            combination = current.word + ending_to_test + next_.word
            deinflict = Deinflect.get_ending(combination, current)
            if deinflict is not None:
                ending.char_indices[1] = next_.char_indices[1]
                ending.endings = deinflict.reasons[0]
                ending.word = ending_to_test + next_.word
                ending.grammar = Grammar.MERGED

                # if the word had been split, we want to revert it at this point.
                conjugated_word.word = combination[:-len(ending.word)]
                conjugated_word.char_indices[1] = conjugated_word.char_indices[0] + len(conjugated_word.word)

                last_match = i + 1
        else:
            break
        i += 1
        ending_to_test += next_.word
    return last_match

# splits tokens that are conjugated into a root and an ending
def _split_conjugated_token(conjugated_word, ending,current):
    deinflict = Deinflect.get_ending(current.word, current)
    dictionary = Dictionary.Dictionary().get_dict().dictionary
    not_word = dictionary.get(current.word) is [] #TODO?
    if deinflict is not None and not_word:
        root_len = len(deinflict.root)
        ending.char_indices[0] = conjugated_word.char_indices[0] + root_len
        ending.char_indices[1] = conjugated_word.char_indices[1]
        conjugated_word.char_indices = [conjugated_word.char_indices[0], ending.char_indices[0]]
        conjugated_word.word = current.word[:root_len]
        conjugated_word.root = deinflict.word
        ending.word = current.word[root_len:]
        ending.endings = deinflict.reasons[0]
        ending.grammar = Grammar.MERGED

def _copy_token(original):
    return Token(original.word, original.grammar, original.root, original.char_indices)

def _conjugates(current):
    return current.grammar == Grammar.VERB or current.grammar == Grammar.I_ADJECTIVE or current.grammar == Grammar.AUX_VERB

def _might_be_ending(token):
    return token.grammar in [Grammar.PARTICLE,Grammar.ADVERB,Grammar.AUX_VERB,
                             Grammar.I_ADJECTIVE, Grammar.VERB, Grammar.NA_ADJECTIVE]


def _merge_words_using_dictionary(tokens):
    merged = []
    i = 0
    while i+1 < len(tokens):
        to_add = Token(tokens[i].word,tokens[i].grammar,tokens[i].root,tokens[i].char_indices,tokens[i].endings)
        start = i
        combination = tokens[i].word + tokens[i + 1].word
        combination = normalize_numbers(combination)
        combined_words = [tokens[i].word]
        dict_entry = Dictionary.match(Token(combination), match_pos=False)
        fails = 0
        fail_limit = 2  # this setting dictates how far the system will look ahead to find valid combinations

        while fails < fail_limit:
            if dict_entry and should_merge(combined_words,combination,dict_entry):
                to_add.char_indices = [tokens[start].char_indices[0],tokens[i+1].char_indices[1]]
                to_add.root = dict_entry[0].writings[0]
                to_add.pos = dict_entry[0].pos[0]
                to_add.word = combination
                fails = 0
            else:
                fails += 1

            i += 1
            if i+1 == len(tokens):
                break
            combination += tokens[i+1].word
            combination = normalize_numbers(combination)
            combined_words.append(tokens[i].word)
            dict_entry = Dictionary.match(Token(combination), match_pos=False)

        merged.append(to_add)
        i += 1 - fails
    merged.append(tokens[i])

    return merged


def should_merge(words,combination, entry):
    if len(words) == 2 and is_small_number(words[0]) and is_day_or_month(words[1]):
        return True
    elif is_wh_question(words[0]):
        return True
    else:  # these tags are accepted since they have a low chance of producing an incorrect result
        return (entry[0].pos[0] == Grammar.NOUN or entry[0].pos[0] == Grammar.PRONOUN) and entry[0].writings[0] == combination


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
