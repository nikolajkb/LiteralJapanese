import Tokenizer


class Sentence:
    def __init__(self, tokens=None, english="", japanese="", index=-1):
        if tokens is None:
            tokens = []
        self.tokens = tokens
        self.english = english
        self.japanese = japanese
        self.index = index


def test_tokenizer():
    return 0


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

        while line and not line == "\n":
            pair = line[:-1].split(" ")
            pair = (pair[0], pair[1])
            sentence.tokens.append(pair)
            line = data.readline()

        sentences.append(sentence)

