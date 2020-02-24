import os
import xml.etree.ElementTree as ET
import Word
from Grammar import Grammar
import pickle


class XmlReader:
    dictionary = None

    def get_dict(self):
        if XmlReader.dictionary is not None:
            return XmlReader.dictionary

        dictionary = load_dictionary()
        if dictionary is not None:
            XmlReader.dictionary = dictionary
            return dictionary

        print("Reading dictionary...")
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir, '..', 'data', 'JMdict_e')
        tree = ET.parse(file_name)
        root = tree.getroot()

        dictionary = {}

        for entry in root:
            word = Word.make_empty()

            k_ele = entry.find("k_ele")
            if k_ele is not None:
                for keb in k_ele.findall("keb"):
                    word.writings.append(keb.text)

            r_ele = entry.find("r_ele")
            if r_ele is not None:
                for reb in r_ele.findall("reb"):
                    word.writings.append(reb.text)

            sense = entry.find("sense")
            for gloss in sense.findall("gloss"):
                word.meanings.append(gloss.text)

            for pos in sense.findall("pos"):
                word.pos.append(make_grammar(pos.text))

            for writing in word.writings:
                if dictionary.get(writing) is None:
                    dictionary[writing] = [word]
                else:
                    dictionary[writing].append(word)

        XmlReader.dictionary = dictionary
        print("done")
        save_dictionary(dictionary)
        return dictionary


def save_dictionary(dictionary):
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '..', 'data', 'JMdict_e_obj.obj')
    file_handler = open(file_name, "wb")
    pickle.dump(dictionary, file_handler)


def load_dictionary():
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '..', 'data', 'JMdict_e_obj.obj')
    try:
        file_handler = open(file_name, "rb")
        dictionary = pickle.load(file_handler)
        return dictionary
    except IOError:
        return None


def make_grammar(tag):
    if tag.startswith("v"):
        return Grammar.VERB

    return {
        "noun (common) (futsuumeishi)": Grammar.NOUN,
        "adjective (keiyoushi)": Grammar.I_ADJECTIVE,
        "adjective (keiyoushi) - yoi/ii class": Grammar.I_ADJECTIVE,
        "adjectival nouns or quasi-adjectives (keiyodoshi)": Grammar.NA_ADJECTIVE,
        "pre-noun adjectival (rentaishi)": Grammar.PRE_NOUN,
        "`taru' adjective": Grammar.NA_ADJECTIVE,
        "noun or verb acting prenominally": Grammar.NOUN,
        "adverb (fukushi)": Grammar.ADVERB,
        "adverb taking the `to' particle": Grammar.ADVERB,
        "auxiliary verb": Grammar.AUX_VERB,
        "conjunction": Grammar.CONJUNCTION,
        "suffix": Grammar.SUFFIX,
        "proper noun": Grammar.NOUN,
        "pronoun": Grammar.PRONOUN,
        "interjection (kandoushi)": Grammar.INTERJECTION,
        "prefix": Grammar.PREFIX,
        "word usually written using kanji alone": Grammar.USUALLY_KANJI,
        "word usually written using kana alone": Grammar.USUALLY_KANA

    }.get(tag, Grammar.NOT_IN_SWITCH)
