from nltk.tokenize import sent_tokenize
from gensim.parsing.preprocessing import remove_stopwords, strip_multiple_whitespaces, preprocess_string, strip_punctuation, strip_numeric
from collections import defaultdict
import pickle


filters = [lambda x: x.lower(), strip_numeric, strip_punctuation, strip_multiple_whitespaces, remove_stopwords]
file_name = r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\wiki_dump\wiki_matrixs.mat"


def zero():
    return 0

def zero_dict():
    return defaultdict(zero)


def create_matrix():
    wiki_path = r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\wiki_dump\wiki.20200412.en\wiki.20200412.en"
    file = open(wiki_path,encoding="utf-8")
    line = file.readline()
    line_nr = 0
    sparse_matrix = defaultdict(zero_dict)
    article = ""
    while line:
        line_nr += 1
        line = line[:-1]
        if is_heading(line) and article != "":
            parse_article(article,sparse_matrix)
            article = ""
        else:
            article += " " + line

        if line_nr > 1000000:
            break
        if line_nr % 1000 == 0:
            print(line_nr)
        line = file.readline()
    save_matrix(sparse_matrix)
    return sparse_matrix


def parse_article(article,matrix):
    sentences = sent_tokenize(article)
    for sentence in sentences:
        words = preprocess_string(sentence, filters)
        for w1 in words:
            for w2 in words:
                if w1 != w2:
                    matrix[w1][w2] += 1


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
        return matrix
    except IOError:
        return None


