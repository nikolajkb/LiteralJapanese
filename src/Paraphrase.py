import os
import re
from Database import Database


def _parse_ppdb():
    print("loading paraphrase database")
    database = Database("ppdb_small.db")
    if database.is_empty():
        print("database not found")
        print("creating database, this might take a while...")
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        ppdb_path = os.path.join(file_dir, "..", "data", "PPDB", "ppdb-2.0-s-all")
        ppdb = open(ppdb_path, "r")

        line = ppdb.readline()
        while line:
            split = line.split("|||")
            phrase = _clean(split[1])
            paraphrase = _clean(split[2])

            database.add_to_list(phrase,paraphrase)
            line = ppdb.readline()

        database.write_to_disk()
    return database


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



