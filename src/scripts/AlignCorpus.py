import os
import Tokenizer
import nltk


def from_ud_pud():
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '..', "data","ud", "UD_Japanese-PUD","ja_pud-ud-test.conllu")
    file_name = os.path.abspath(file_name)
    input_corpus = open(file_name, "r", encoding="utf-8")
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '..', "data", "ja_pud.align")
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


def from_JParaCrawl():
    file_name = os.path.abspath(r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\JParaCrawl\en-ja.bicleaner05.txt")
    input_file = open(file_name,"r",encoding="utf-8")
    file_name = os.path.abspath(r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\JPara2.align")
    output_file = open(file_name,"w+",encoding="utf-8")
    line = input_file.readline()
    total = 0
    i = 0
    while line:
        split = line.split("\t")
        jp = split[3]
        jp = jp[:-1]
        en = split[2]
        (jp_tokens,en_tokens) = make_tokens(jp,en)

        output_file.write(jp_tokens + " ||| " + en_tokens + "\n")

        i += 1
        total += 1
        if i == 10000:
            if total > 1000000:
                output_file.close()
                break
            print(total)
            i = 0
        line = input_file.readline()


def from_KFTT():
    file_name = os.path.abspath(r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\KFTT_corpus\kyoto-train.ja")
    input_jp = open(file_name, "r", encoding="utf-8")
    file_name = os.path.abspath(r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\KFTT_corpus\kyoto-train.en")
    input_en = open(file_name, "r", encoding="utf-8")
    file_name = os.path.abspath(r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\KFTT.parallel")
    output_file = open(file_name, "w+", encoding="utf-8")

    line_jp = input_jp.readline()
    line_en = input_en.readline()
    while line_jp:
        line_jp = line_jp[:-1]
        line_en = line_en[:-1]
        (jp,en) = make_tokens(line_jp,line_en)
        output_file.write(make_parallel_line(jp,en))
        line_jp = input_jp.readline()
        line_en = input_en.readline()


def make_parallel_line(jp,en):
    return jp + " ||| " + en + "\n"

def make_tokens(jp,en):
    jp_tokens = Tokenizer.get_tokens(jp)
    jp_tokens = [t.word for t in jp_tokens]
    en_tokens = nltk.tokenize.word_tokenize(en)

    jp_tokens = " ".join(jp_tokens)
    en_tokens = " ".join(en_tokens)
    return jp_tokens, en_tokens
