import os
import re


def _parse_ppdb():
    print("loading paraphrase database")
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_path = os.path.join(file_dir, "..", "data", "PPDB", "ppdb-2.0-s-all")
    file = open(file_path, "r")

    dictionary = {}
    line = file.readline()
    while line:
        split = line.split("|||")
        phrase = _clean(split[1])
        paraphrase = _clean(split[2])

        current = dictionary.get(phrase)
        if current is None:
            dictionary[phrase] = {paraphrase}
        else:
            current.add(paraphrase)
        line = file.readline()

    return dictionary


def _clean(string):
    string = re.sub("\[[^\]]*\]", "", string)
    return string.strip()


class Ppdb():
    ppdb = None

    @staticmethod
    def get_ppdb():
        if Ppdb.ppdb is None:
            Ppdb.ppdb = _parse_ppdb()

        return Ppdb.ppdb



