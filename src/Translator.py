import getopt
import Tokenizer
import Dict_Translator
import Tests
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
            Tests.test_tokenizer()


if __name__ == "__main__":
    main(sys.argv[1:])



