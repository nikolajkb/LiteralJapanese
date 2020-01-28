import Tokenizer
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


def calc_score(gold_len, system_len, correct):
    precision = correct / system_len
    recall = correct / gold_len
    f1 = 2 * correct / (system_len + gold_len)
    print("precision:", precision)
    print("recall:", recall)
    print("f1:", f1)
    print("\n")


def test_tokenizer():
    sentences = read_test_data()

    for sentence in sentences:
        print(" - sentence", sentence.index, " - ")
        tokens = Tokenizer.get_tokens(sentence.japanese)
        gold_tokens = sentence.tokens
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

        calc_score(len(gold_tokens), len(tokens), correct)




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
        while line and not line == "\n":
            pair = line[:-1].split(" ")
            sentence.tokens.append(SentenceToken(pair[0], pair[1], (index, index + pair[0].__len__())))
            index += pair[0].__len__()
            line = data.readline()

        sentences.append(sentence)
        line = data.readline()

    return sentences
