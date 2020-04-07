import Constants
import os
import Dictionary
import Grammar


# input: a dictionary as defined in Dictionary.py
def add_frequency(dictionary):
    freq_file_path = os.path.join(Constants.PROJECT_DIR, "..", "data", "LeedsWordFrequency", "44492-japanese-words-latin-lines-removed.txt")
    frequencies = open(freq_file_path,"r", encoding="utf-8")

    line = frequencies.readline()
    i = 0
    while line:
        i += 1
        line = line[:-1]
        is_hiragana = Grammar.is_hiragana(line)

        entries = dictionary.get(line,[])
        if is_hiragana:
            entries = [e for e in entries if Grammar.Grammar.USUALLY_KANA in e.misc]
        else:
            entries = [e for e in entries if Grammar.Grammar.USUALLY_KANA not in e.misc]

        for entry in entries:
            entry.priority = i

        line = frequencies.readline()
