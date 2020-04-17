import PrintTools
import Tokenizer
import Translator
import Tests
import sys
import argparse
import Constants
import WikiMatrix


def translate(text, translation=None):
    #translation = GoogleTranslate.translate_google(text)
    #translation = translation[:1].lower() + translation[1:]
    translation = None
    tokens = Tokenizer.get_tokens(text)
    translations = Translator.translate(tokens,translation=translation)
    return translations


def batch_translate(input_file, output_file):
    input_file = open(input_file,encoding="utf-8")
    line = input_file.readline()
    while line:
        translation = translate(line[:-1])
        PrintTools.write_to_file(translation,output_file)

        line = input_file.readline()


def start_interactive():
    print("Type Japanese sentences, press enter to translate")
    print("Enter q to quit")
    while True:
        command = input("> ")
        if command == "q" or command == "ｑ":
            sys.exit()
        else:
            print(command)
            print(translate(command))


def main(argv):
    #Constants.WIKI_STATS = WikiMatrix.load_matrix()
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--translate",type=str,help="translates a Japanese sentence to English and writes it to a file")
    parser.add_argument("--batch-translate",action="store_true", help="translates each line in a file and writes translations to a file")
    parser.add_argument("--test",type=str, help="tests translation system using file containing test cases")
    parser.add_argument("--tt", type=str, help="tests the tokenizing using a file")
    parser.add_argument("-v","--verbose", action="store_true")
    parser.add_argument("-i", "--interactive", action="store_true", help="run an interactive version of the system")
    parser.add_argument("-p", "--paraphrase", action="store_true", help="count translations as correct during testing if they are paraphrases of the gold translation")
    parser.add_argument("--input", type=str, help="input file for translation", default=None)
    parser.add_argument("--output", type=str, help="output file for translation", default=None)

    args = parser.parse_args()

    Constants.VERBOSE = args.verbose
    Constants.PARAPHRASE = args.paraphrase

    if args.interactive:
        start_interactive()
    if args.translate:
        if args.output and args.translate != "":
            PrintTools.write_to_file(translate(args.translate), args.output)
        else:
            print("Please specify text to translate and output file")
    elif args.batch_translate:
        if args.input and args.output:
            batch_translate(args.input, args.output)
        else:
            print("Please specify input and output files")
    elif args.test:
        Tests.test_translator(args.test)
    elif args.tt:
        Tests.test_tokenizer(args.tt)
    else:
        print("Incorrect arguments")
        parser.print_help()


if __name__ == "__main__":
    main(sys.argv[1:])



