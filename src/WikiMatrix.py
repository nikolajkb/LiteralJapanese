from nltk.tokenize import sent_tokenize
from gensim.parsing.preprocessing import remove_stopwords, strip_multiple_whitespaces, preprocess_string, strip_punctuation, strip_numeric
from scipy.sparse import coo_matrix, save_npz, load_npz
import numpy as np
import pickle


filters = [lambda x: x.lower(), strip_numeric, strip_punctuation, strip_multiple_whitespaces]  # stopwords not removed
file_name = r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\wiki_dump\wiki_matrix"
matrix_file = file_name+".npz"
vocab_file = file_name+".vocab"


class OneIter:
    def __init__(self,limit):
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        return 1


class WordStats:
    def __init__(self):
        self.row = []
        self.column = []
        self.vocabulary = {}  # key = word, val = index, frequency
        self.data_count = 0

    def add(self,w1,w2):
        i1 = self.add_to_vocab(w1)
        i2 = self.add_to_vocab(w2)
        self.row.append(i1)
        self.column.append(i2)
        self.data_count += 1

    def add_to_vocab(self,word):
        index = self.vocabulary.setdefault(word,len(self.vocabulary))
        return index

    def data(self):
        # creates an array of only 1s. Using iterator avoids making a temp array
        return np.fromiter(OneIter(self.data_count),dtype=int,count=self.data_count)

    def rows(self):
        return np.array(self.row)

    def columns(self):
        return np.array(self.column)


def create_matrix():
    wiki_path = r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\wiki_dump\wiki.20200412.en\wiki.20200412.en"
    file = open(wiki_path,encoding="utf-8")
    line = file.readline()
    line_nr = 0
    stats = WordStats()
    article = ""
    while line:
        line_nr += 1
        line = line[:-1]
        if is_heading(line) and article != "":
            parse_article(article,stats)
            article = ""
        else:
            article += " " + line

        if line_nr > 100000:
            break
        if line_nr % 1000 == 0:
            print(line_nr)
        line = file.readline()
    save_matrix(stats)
    return stats


def parse_article(article,stats):
    sentences = sent_tokenize(article)
    for sentence in sentences:
        words = preprocess_string(sentence, filters)
        for w1 in words:
            for w2 in words:
                if w1 != w2:
                    stats.add(w1,w2)


def is_heading(text):
    return len(text) < 40 and "." not in text and "," not in text


def save_matrix(stats):
    print("creating matrix")
    matrix = coo_matrix((stats.data(), (stats.rows(), stats.columns())))
    print("converting to csr")
    matrix = matrix.tocsr()
    save_npz(matrix_file, matrix)

    vocab_file_handler = open(vocab_file, "wb")
    pickle.dump(stats.vocabulary, vocab_file_handler)


def load_matrix():
    try:
        return load_npz(matrix_file)
    except IOError:
        return None


def load_vocab():
    file_handler = open(vocab_file, "rb")
    vocab = pickle.load(file_handler)
    return vocab


def get_co_occurrence(matrix,vocab,w1,w2):
    return matrix[vocab[w1][0]][vocab[w2][0]]


