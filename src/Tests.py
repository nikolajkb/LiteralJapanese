from typing import List

import Equality
import LevenshteinDistance
import Constants
import Tokenizer
import LiteralJapanese
from PrintTools import print_translated_sentence, print_translated_sentence_v
from Similarity import Similarity, init_similarity

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


class TokenScore:
    def __init__(self, gold_len, system_len, correct):
        self.precision = correct / system_len
        self.recall = correct / gold_len
        self.f1 = 2 * correct / (system_len + gold_len)

    def print(self):
        print("precision:", self.precision)
        print("recall:", self.recall)
        print("f1:", self.f1)
        print("")


class TranslationScore:
    def __init__(self, gold_len, errors):
        (del_e,ins_e,sub_e) = errors
        self.total_errors = LevenshteinDistance.total(errors)
        self.deletions = del_e
        self.insertions = ins_e
        self.substitutions = sub_e
        self.error_rate = LevenshteinDistance.total(errors) / gold_len
        self.del_rate = del_e / gold_len
        self.ins_rate = ins_e / gold_len
        self.sub_rate = sub_e / gold_len

    @staticmethod
    def make_average(scores):
        final_score = TranslationScore(1, (1,1,1))
        final_score.total_errors = sum(s.total_errors for s in scores) / len(scores)
        final_score.deletions = sum(s.deletions for s in scores) / len(scores)
        final_score.insertions = sum(s.insertions for s in scores) / len(scores)
        final_score.substitutions = sum(s.substitutions for s in scores) / len(scores)
        final_score.error_rate = sum(s.error_rate for s in scores) / len(scores)
        final_score.del_rate = sum(s.del_rate for s in scores) / len(scores)
        final_score.ins_rate = sum(s.ins_rate for s in scores) / len(scores)
        final_score.sub_rate = sum(s.sub_rate for s in scores) / len(scores)

        return final_score

    def print(self):
        print("total errors:", self.total_errors)
        print("deletions:", self.deletions)
        print("insertions:", self.insertions)
        print("substitutions:", self.substitutions)
        print("error rate:", self.error_rate)
        print("deletion rate:", self.del_rate)
        print("insertion rate:", self.ins_rate)
        print("substitution rate:", self.sub_rate)


def test_tokenizer(file_path):
    sentences = read_test_data(file_path)
    scores = []

    for sentence in sentences:
        score = calc_sentence_score(sentence)
        scores.append(score)

    final_score = make_average_score(scores)

    print("#### average result ####")
    final_score.print()
    return final_score


def test_translator(file_path):
    sentences = read_test_data(file_path)
    init_similarity()

    scores = []

    print("translating sentences\n")
    if Constants.VERBOSE:
        print("print format:")
        print("- sentence x | score: (deletions, insertions, substitutions) -")
        print("gold tokens")
        print("gold translations")
        print("system tokens")
        print("system translations\n")
    for sentence in sentences:
        system = LiteralJapanese.translate(sentence.japanese, translation=sentence.english)
        gold = sentence.tokens
        score = translation_sentence_score(gold, system)
        if Constants.VERBOSE:
            print_translated_sentence_v(sentence, system, gold, score)
        scores.append(TranslationScore(len(gold), score))

    avg = TranslationScore.make_average(scores)
    print("#### average result (Levenshtein distance) ####")
    avg.print()

    return avg


def make_average_score(scores):
    final_score = TokenScore(1, 1, 1)
    final_score.precision = sum(s.precision for s in scores) / len(scores)
    final_score.recall = sum(s.recall for s in scores) / len(scores)
    final_score.f1 = sum(s.f1 for s in scores) / len(scores)

    return final_score


def translation_sentence_score(gold, system):
    gold = [x.english for x in gold]
    system = [s.english for s in system]

    return LevenshteinDistance.distance(gold, system)


def calc_sentence_score(sentence):
    if sentence.index == 97:
        print("")
    tokens = Tokenizer.get_tokens(sentence.japanese.strip())
    gold_tokens = sentence.tokens

    print(" - sentence", sentence.index, " - ")
    print("system:", [t.word for t in tokens])
    print("gold:  ", [t.japanese for t in gold_tokens])

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

    score = TokenScore(len(gold_tokens), len(tokens), correct)
    score.print()
    return score


def print_equalities():
    Constants.SIMILARITY = Similarity()
    Constants.PARAPHRASE = True
    sentences = read_test_data(r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\sentences_dev.txt")
    for sentence in sentences:
        print([t.english for t in sentence.tokens])
        translations = LiteralJapanese.translate(sentence.japanese)
        print([t.english for t in translations])
        for translation in translations:
            for token in sentence.tokens:
                (equal,rule) = Equality.equals_rule(token.english,translation[1])
                if equal:
                    print(token.english + " = " + translation.english + "\t" + "("+rule+")")


# read test data into Sentence object
def read_test_data(file_path):
    linenr = 1
    try:
        print("reading test data")
        data = open(file_path, "r", encoding="utf-8")
        linenr += 1
        line = data.readline()
        sentences = []
        while line:
            sentence = Sentence()
            sentence.index = int(line[1:-1])
            linenr += 1
            line = data.readline()
            sentence.japanese = line[4:-1]
            linenr += 1
            line = data.readline()
            sentence.english = line[4:-1]
            linenr += 1
            line = data.readline()

            index = 0
            while line and not line == "\n":  # read each token and split into English and Japanese
                line = line.replace("\n", "")
                pair = line.split("\t", 1)
                pair = add_spaces(pair)
                sentence.tokens.append(SentenceToken(pair[0], pair[1], (index, index + len(pair[0]) )))
                index += len(pair[0])
                linenr += 1
                line = data.readline()

            sentences.append(sentence)
            linenr += 1
            line = data.readline()
        return sentences
    except:
        print("Error in reading test data around line "+str(linenr))
        exit(-1)


def add_spaces(pair):
    if pair[0] == "\space":
        pair[0] = " "
    if pair[1] == "\space":
        pair[1] = " "
    return pair
