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

class Score:
    def __init__(self, gold_len, system_len, correct):
        self.precision = correct / system_len
        self.recall = correct / gold_len
        self.f1 = 2 * correct / (system_len + gold_len)

    def print(self):
        print("precision:", self.precision)
        print("recall:", self.recall)
        print("f1:", self.f1)
        print("\n")

def test_tokenizer():
    sentences = read_test_data()
    scores = []

    for sentence in sentences:
        print(" - sentence", sentence.index, " - ")
        tokens = Tokenizer.get_tokens(sentence.japanese.strip())
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

        scores.append(Score(len(gold_tokens), len(tokens), correct))

    final_precision = sum(s.precision for s in scores) / len(scores)
    final_recall = sum(s.recall for s in scores) / len(scores)
    final_f1 = sum(s.f1 for s in scores) / len(scores)
    print("#### result ####")
    print("precision:", final_precision)
    print("recall:", final_recall)
    print("f1:", final_f1)





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
