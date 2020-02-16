from typing import List

import Tokenizer
import Translator

start = 0
end = 1


class Sentence:
    def __init__(self, tokens=None, english="", japanese="", index=-1):
        if tokens is None:
            tokens = []
        self.tokens = tokens
        self.english = english
        self.japanese = japanese
        self.index = index


class SentenceToken:
    def __init__(self, japanese, english, indices):
        self.english = english
        self.japanese = japanese
        self.indices = indices


class Score:
    def __init__(self, gold_len, system_len, correct):
        self.precision = correct / system_len
        self.recall = correct / gold_len
        self.f1 = 2 * correct / (system_len + gold_len)

    def print(self):
        print("precision:", self.precision)
        print("recall:", self.recall)
        print("f1:", self.f1)
        print("")


def test_tokenizer():
    sentences = read_test_data()
    scores = []

    for sentence in sentences:
        score = calc_sentence_score(sentence)
        scores.append(score)

    final_score = make_average_score(scores)

    print("#### average result ####")
    final_score.print()
    return final_score


def test_translator():
    sentences = read_test_data()
    sentences = merge_word_endings(sentences)

    scores = []

    for sentence in sentences:
        system = Translator.translate(sentence.japanese)
        gold = sentence.tokens
        print_translated_sentence(sentence, system, gold)
        scores.append(translation_sentence_score(gold, system))

    final_score = make_average_score(scores)

    print("#### average result ####")
    final_score.print()

    return final_score


def print_translated_sentence(sentence, system, gold):
    print(" - sentence", sentence.index, " - ")

    max_len = max(len(gold), len(system))
    for i in range(max_len):
        if i < len(gold):
            g = gold[i]
        else:
            g = SentenceToken("", "", "")
        if i < len(system):
            s = system[i]
        else:
            s = ("", "")

        print(g.japanese.ljust(8-len(g.japanese)), " ", g.english.ljust(30-len(g.english)), s[1])


def make_average_score(scores):
    final_score = Score(1, 1, 1)
    final_score.precision = sum(s.precision for s in scores) / len(scores)
    final_score.recall = sum(s.recall for s in scores) / len(scores)
    final_score.f1 = sum(s.f1 for s in scores) / len(scores)

    return final_score


def translation_sentence_score(gold, system):
    correct = 0

    for gold_token, system_token in zip(gold, system):
        if gold_token.english == system_token[1]:
            correct += 1

    return Score(len(gold), len(system), correct)


def merge_word_endings(sentences):
    for sentence in sentences:
        sentence.tokens = merge_token_list(sentence.tokens)

    return sentences


def merge_token_list(tokens: List[SentenceToken]):  # TODO this is kinda ugly code
    merged = []
    i = 0
    while i < len(tokens):
        if is_ending(tokens[i]):
            ending = tokens[i]
            i += 1
            while i < len(tokens) and is_ending(tokens[i]):
                ending = merge_tokens(ending, tokens[i])
                i += 1
            merged.append(ending)
            i -= 1
        elif not is_ending(tokens[i]):
            merged.append(tokens[i])
        i += 1

    return merged


def is_ending(token):
    return token.english.startswith("-")


def merge_tokens(t1, t2):
    (min_i, _) = t1.indices
    (_, max_i) = t2.indices
    return SentenceToken(t1.japanese + t2.japanese, t1.english + t2.english, (min_i, max_i))


def calc_sentence_score(sentence):
    tokens = Tokenizer.get_tokens(sentence.japanese.strip())
    gold_tokens = sentence.tokens

    print(" - sentence", sentence.index, " - ")
    print("system:", [t.word for t in tokens])
    print("gold:", [t.japanese for t in gold_tokens])

    correct, gi, si = 0, 0, 0
    while gi < len(gold_tokens) and si < len(tokens):
        if tokens[si].char_indices[start] < gold_tokens[gi].indices[start]:
            si += 1
        elif gold_tokens[gi].indices[start] < tokens[si].char_indices[start]:
            gi += 1
        else:
            correct += gold_tokens[gi].indices[end] == tokens[si].char_indices[end]
            si += 1
            gi += 1

    score = Score(len(gold_tokens), len(tokens), correct)
    score.print()
    return score


# read test data into Sentence object
def read_test_data():
    data = open("../data/translations.txt", "r", encoding="utf-8")
    line = data.readline()
    sentences = []
    while line:
        sentence = Sentence()
        sentence.index = int(line[1:-1])
        line = data.readline()
        sentence.japanese = line[4:-1]
        line = data.readline()
        sentence.english = line[4:-1]
        line = data.readline()

        index = 0
        while line and not line == "\n":  # read each token and split into English and Japanese
            pair = line[:-1].split(" ", 1)
            sentence.tokens.append(SentenceToken(pair[0], pair[1], (index, index + len(pair[0]) )))
            index += len(pair[0])
            line = data.readline()

        sentences.append(sentence)
        line = data.readline()

    return sentences
