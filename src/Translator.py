import getopt

import PrintTools
import Tokenizer
import Dict_Translator
import Tests
from Grammar import Grammar
from XmlReader import XmlReader
import LevenshteinDistance
import sys
import argparse


def translate(text):
    tokens = Tokenizer.get_tokens(text)
    translations = Dict_Translator.translate(tokens)
    return translations


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--translate",type=str,help="translates a Japanese sentence to English and writes it to a file")
    parser.add_argument("file", type=str)

    args = parser.parse_args()
    if args.translate:
        if args.file:
            PrintTools.write_to_file(translate(args.translate), args.file)
        else:
            print("no output file specified")



def print_tokenization():
    data = open("../data/translations.txt", "r", encoding="utf-8")
    line = data.readline()
    while line:
        if line.startswith("#jp"):
            split = line.split(" ")
            print(" ")
            print(split[1])
            print(Tokenizer._tokenize(split[1]))
        line = data.readline()


if __name__ == "__main__":
    main(sys.argv[1:])



