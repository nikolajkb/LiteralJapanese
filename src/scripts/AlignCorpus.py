import os
import Tokenizer
import nltk


def from_ud_pud():
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '..', "data","ud", "UD_Japanese-PUD","ja_pud-ud-test.conllu")
    file_name = os.path.abspath(file_name)
    input_corpus = open(file_name, "r", encoding="utf-8")
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '..', "data", "aligned_corpus")
    aligned_output = open(file_name,"w+", encoding="utf-8")

    line = input_corpus.readline()
    while line:
        if line.startswith("# text"):
            jp = line[9:-1]
            line = input_corpus.readline()
            en = line[12:-1]

            jp_tokens = Tokenizer.get_tokens(jp)
            jp_tokens = [t.word for t in jp_tokens]
            en_tokens = nltk.tokenize.word_tokenize(en)

            jp_tokens = " ".join(jp_tokens)
            en_tokens = " ".join(en_tokens)

            aligned_output.write(jp_tokens + " ||| " + en_tokens + "\n")

        line = input_corpus.readline()
