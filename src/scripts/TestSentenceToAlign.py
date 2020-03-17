import nltk

import Tokenizer

input_path = r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\sentences_dev.txt"
output_path = r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\sentences_dev.align"
input_file = open(input_path,"r",encoding="utf-8")
output_file = open(output_path,"w+",encoding="utf-8")

line = input_file.readline()
while line:
    if line.startswith("#jp"):
        jp = line[4:-1]
        jp = Tokenizer.tokenize_sudachi(jp)
        jp = [t.word for t in jp]
        jp = " ".join(jp)
        line = input_file.readline()
        en = line[4:-1]
        en = nltk.tokenize.word_tokenize(en)
        en = " ".join(en)
        output_file.write(jp + " ||| " + en + "\n")
    line = input_file.readline()
