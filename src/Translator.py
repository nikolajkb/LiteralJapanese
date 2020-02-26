import getopt
import Tokenizer
import Dict_Translator
import Tests
from Grammar import Grammar
from XmlReader import XmlReader
import LevenshteinDistance
import sys


def translate(text):
    tokens = Tokenizer.get_tokens(text)
    translations = Dict_Translator.translate(tokens)
    return translations


def main(argv):
    options, args = getopt.getopt(argv, "t:o:p:b:dh", ["file="])

    for option, arg in options:
        if option == "-h":
            print("-t = translate text TODO")
            print("-o = tokenize text")
            print("-p = test tokens with file TODO")
            print("-b = test translations with file TODO")
            print("-d = run dev code (for testing)")
        elif option == "-o":
            print(arg)
            print(Tokenizer.get_tokens(arg))
        elif option == "-d":
            print(Tokenizer.get_tokens("いいえ、いらなくなったので、昨日燃やしてしまいました。"))
            Tests.test_translator()


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



