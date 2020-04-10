import os
import re
from enum import Enum
from Database import Database


class Size(Enum):
    SMALL = "ppdb-2.0-s-all"
    MEDIUM = "ppdb-2.0-m-all"
    LARGE = "ppdb-2.0-l-all"


PPDB_SIZE = Size.SMALL

def _parse_ppdb():
    print("loading paraphrase database")
    database = Database(PPDB_SIZE.value+".db")
    if database.is_empty():
        print("database not found")
        print("creating database, this might take a while...")
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        ppdb_path = os.path.join(file_dir, "..", "data", "PPDB", PPDB_SIZE.value)
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



