import os
import xml.etree.ElementTree as ET
import Word
from Grammar import Grammar


class XmlReader:
    dictionary = None

    def get_dict(self):
        if XmlReader.dictionary is not None:
            return XmlReader.dictionary

        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir, '..', 'data', 'JMdict_e')
        tree = ET.parse(file_name)
        root = tree.getroot()

        dictionary = {}

        for entry in root:
            word = Word.make_empty()
            k_ele = entry.find("k_ele")
            sense = entry.find("sense")
            if k_ele is None or sense is None:
                continue

            for keb in k_ele.findall("keb"):
                word.writings.append(keb.text)

            for gloss in sense.findall("gloss"):
                word.meanings.append(gloss.text)

            for pos in sense.findall("pos"):
                word.pos = make_grammar(pos.text)

            for writing in word.writings:
                dictionary[writing] = word

        XmlReader.dictionary = dictionary
        return dictionary


def make_grammar(tag):
    return {
        "noun (common) (futsuumeishi)": Grammar.NOUN,

    }.get(tag, Grammar.NOT_IN_SWITCH)
