from nltk.tokenize import sent_tokenize
from gensim.parsing.preprocessing import remove_stopwords, strip_multiple_whitespaces, preprocess_string, strip_punctuation, strip_numeric
from collections import defaultdict
import numpy as np
from scipy.sparse import lil_matrix
import pickle
import psutil
import os
import Constants

filters = [lambda x: x.lower(), strip_numeric, strip_punctuation, strip_multiple_whitespaces]  # stopwords not removed
file_name = os.path.join(Constants.PROJECT_DIR,"..","data","wiki_dump","wiki_matrix_obj.wstats")
wiki_path = os.path.join(Constants.PROJECT_DIR, "..","data","wiki_dump","wiki.20200412.en","wiki.20200412.en")
line_limit = 500000

low_freq_path = os.path.join(Constants.PROJECT_DIR ,"..","data","wiki_dump","low_freq_words.bin")
low_freq = set(pickle.load(open(low_freq_path,"rb")))


def int_dict():
    return defaultdict(int)


class WordStats:
    def __init__(self):
        self.matrix = defaultdict(int_dict)
        self.frequencies = defaultdict(int)

    def add(self,w1,w2):
        if w1 not in low_freq and w2 not in low_freq:
            self.matrix[w1][w2] += 1
            self.frequencies[w1] += 1

    def convert_to_scipy_matrix(self):
        matrix = lil_matrix((len(self.frequencies),len(self.frequencies)), dtype=np.int16)
        indices = {}
        i = 0
        for (w1,row) in self.matrix.items():
            indices.setdefault(w1,len(indices))
            j = 0
            for (w2,frequency) in row.items():
                matrix[i,j] = frequency
                j += 1
            i += 1

        return matrix.tocsr(),indices


def create_matrix():
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

        if line_nr > line_limit:
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


def save_matrix(matrix):
    file_handler = open(file_name, "wb")
    pickle.dump(matrix, file_handler)


def load_matrix():
    try:
        file_handler = open(file_name, "rb")
        matrix = pickle.load(file_handler)
        file_handler.close()
        print("loaded")
        return matrix
    except IOError:
        return None


def print_mem():
    process = psutil.Process(os.getpid())
    print(process.memory_info().rss/1000000,"MB")
