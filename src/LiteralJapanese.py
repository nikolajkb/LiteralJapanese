import getopt

import PrintTools
import Tokenizer
import Translator
import Tests
from Grammar import Grammar
from Dictionary import Dictionary
import LevenshteinDistance
import sys
import argparse
import Settings


def translate(text, translation=None):
    tokens = Tokenizer.get_tokens(text)
    translations = Translator.translate(tokens,translation=translation)
    return translations


def start_interactive():
    print("Type Japanese sentences, press enter to translate")
    while True:
        command = input("> ")
        if command == "q" or command == "ｑ":
            sys.exit()
        else:
            print(command)
            print(translate(command))


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--translate",type=str,help="translates a Japanese sentence to English and writes it to a file")
    parser.add_argument("file", nargs="?", type=str, default=None)
    parser.add_argument("--test",type=str, help="tests translation system using file containing test cases")
    parser.add_argument("--tt", type=str, help="tests the tokenizing using a file")
    parser.add_argument("-v","--verbose", action="store_true")
    parser.add_argument("-i", "--interactive", action="store_true", help="run an interactive version of the system")
    parser.add_argument("-p", "--paraphrase", action="store_true", help="count translations as correct during testing if they are paraphrases of the gold translation")

    args = parser.parse_args()

    Settings.VERBOSE = args.verbose
    Settings.PARAPHRASE = args.paraphrase

    if args.interactive:
        start_interactive()
    if args.translate:
        if args.file:
            PrintTools.write_to_file(translate(args.translate), args.file)
        else:
            print("no output file specified")
    elif args.test:
        Tests.test_translator(args.test)
    elif args.tt:
        Tests.test_tokenizer(args.tt)
    else:
        parser.print_help()


def print_tokenization():
    data = open("../data/translations.txt", "r", encoding="utf-8")
    line = data.readline()
    while line:
        if line.startswith("#jp"):
            split = line.split(" ")
            print(" ")
            print(split[1])
            print(Tokenizer.tokenize_sudachi(split[1]))
        line = data.readline()


if __name__ == "__main__":
    main(sys.argv[1:])



