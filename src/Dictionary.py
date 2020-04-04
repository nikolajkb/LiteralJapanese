import os
import xml.etree.ElementTree as ET
import Word
from Grammar import Grammar, is_hiragana, is_katakana
import pickle
import WordFrequency


class Dictionary:
    dictionary = None
    pn_dictionary = None

    @staticmethod
    def get_dict():
        if Dictionary.dictionary is not None:
            return Dictionary

        dictionary = load_dictionary("JMdict_e")
        pn_dictionary = load_dictionary("JMnedict")
        if dictionary is not None and pn_dictionary is not None:
            Dictionary.dictionary = dictionary
            Dictionary.pn_dictionary = pn_dictionary
            return Dictionary

        print("Reading dictionary...")
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir, '..', 'data',"JMdict_dictionary", 'JMdict_e')
        tree = ET.parse(file_name)
        root = tree.getroot()

        dictionary = {}

        for entry in root:
            word = Word.make_empty()

            # shared
            k_ele_list = entry.findall("k_ele")
            for k_ele in k_ele_list:
                for keb in k_ele.findall("keb"):
                    word.writings.append(keb.text)

                for ke_pri in k_ele.findall("ke_pri"):
                    if ke_pri.text.startswith("nf"):
                        word.priority = int(ke_pri.text[2:])

            r_ele_list = entry.findall("r_ele")
            for r_ele in r_ele_list:
                for reb in r_ele.findall("reb"):
                    word.writings.append(reb.text)

                for re_pri in r_ele.findall("re_pri"):
                    if re_pri.text.startswith("nf"):
                        priority = int(re_pri.text[2:])
                        if priority < word.priority:
                            word.priority = priority

            only_kana = True
            for writing in word.writings:
                if not is_hiragana(writing):
                    only_kana = False
                    break
            if only_kana:
                word.misc.append(Grammar.USUALLY_KANA)

            # individual
            first_pos = []
            first_misc = []
            first = True
            sense_list = entry.findall("sense")
            for sense in sense_list:
                word_cpy = Word.copy(word)
                for gloss in sense.findall("gloss"):
                    word_cpy.meanings.append(gloss.text)

                for pos in sense.findall("pos"):
                    word_cpy.pos.append(make_grammar(pos.text))

                for misc in sense.findall("misc"):
                    word_cpy.misc.append(make_grammar(misc.text))

                # the dictionary defines that pos and misc tags count for all senses, unless those senses redefine these.
                if first:
                    first_pos = word_cpy.pos
                    first_misc = word_cpy.misc
                    first = False
                else:
                    if not word_cpy.pos:
                        word_cpy.pos = first_pos

                word_cpy.misc.extend(first_misc)

                # these elements indicate that this sense only applies for some readings/writings
                restrictions = []
                for stagr in sense.findall("stagr"):
                    restrictions.append(stagr.text)
                for stagk in sense.findall("stagk"):
                    restrictions.append(stagk.text)

                if restrictions:
                    word_cpy.writings = restrictions

                _add_to_dictionary(word_cpy,dictionary)

        pn_dict = read_pn_dictionary()
        Dictionary.pn_dictionary = pn_dict
        Dictionary.dictionary = dictionary
        print("done")
        save_dictionary(dictionary, "JMdict_e")
        save_dictionary(pn_dict, "JMnedict")
        return Dictionary


def _add_to_dictionary(word, dictionary):
    for writing in word.writings:
        if dictionary.get(writing) is None:
            dictionary[writing] = [word]
        else:
            dictionary[writing].append(word)


def read_pn_dictionary():
    file_dir = os.path.dirname(os.path.realpath('__file__'))

    file_name = os.path.join(file_dir, '..', 'data',"JMdict_dictionary", 'JMnedict.xml')
    tree = ET.parse(file_name)
    root = tree.getroot()
    dictionary = parse_pn_dict(root)

    file_name = os.path.join(file_dir, '..', 'data',"JMdict_dictionary", 'JMnedict_2.xml')
    tree = ET.parse(file_name)
    root = tree.getroot()
    dictionary2 = parse_pn_dict(root)

    dictionary3 = parse_csv_name_dict()

    dictionary3.update(dictionary2)
    dictionary3.update(dictionary)
    return dictionary3


def parse_csv_name_dict():
    dictionary = {}
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '..', 'data', "Wikipedia_name_corpus", 'data_dict_convert.csv')
    file = open(file_name,"r",encoding="utf-8")
    line = file.readline()
    while line:
        (jp,en) = line[:-1].split(",",1)
        word = Word.make_empty()
        word.meanings.append(en)
        word.writings.append(jp)
        dictionary[jp] = [word]
        line = file.readline()

    return dictionary


def parse_pn_dict(root):
    dictionary = {}
    for entry in root:
        word = Word.make_empty()

        k_ele = entry.find("k_ele")
        if k_ele is not None:
            keb = k_ele.find("keb")
            word.writings.append(keb.text)

        r_ele = entry.find("r_ele")
        if r_ele is not None:
            reb = r_ele.find("reb")
            word.writings.append(reb.text)

        trans = entry.find("trans")
        if trans is not None:
            trans_det = trans.find("trans_det")
            if trans_det is not None:
                word.meanings.append(trans_det.text)

        dictionary[word.writings[0]] = [word]

    return dictionary


def save_dictionary(dictionary, name):
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '..', 'data',"JMdict_dictionary", name + ".obj")
    file_handler = open(file_name, "wb")
    pickle.dump(dictionary, file_handler)
    file_handler.flush()
    file_handler.close()


def load_dictionary(name):
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '..', 'data',"JMdict_dictionary", name + ".obj")
    try:
        file_handler = open(file_name, "rb")
        print("loading dictionary: "+name)
        dictionary = pickle.load(file_handler)
        file_handler.close()
        return dictionary
    except IOError:
        return None


def make_grammar(tag):
    grammar = {
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
        "word usually written using kana alone": Grammar.USUALLY_KANA,
        "adverbial noun (fukushitekimeishi)": Grammar.NOUN,
        "noun, used as a suffix": Grammar.NOUN,
        "noun, used as a prefix": Grammar.NOUN,
        "noun (temporal) (jisoumeishi)": Grammar.NOUN,
        "particle": Grammar.PARTICLE

    }.get(tag, Grammar.NOT_IN_SWITCH)

    if grammar == Grammar.NOT_IN_SWITCH:
        if " verb" in tag:
            grammar = Grammar.VERB

    return grammar


# returns the raw results of a lookup in the dictionary
def get(word):
    return Dictionary.get_dict().dictionary.get(word)


# returns translations from dictionary that match pos/kana
def match(token, match_kana=True, match_pos=True):
    dictionary = Dictionary.get_dict().dictionary
    translations = dictionary.get(token.root)
    if translations:
        if match_pos:
            # attempt to match pos
            pos_match = [t for t in translations if token.grammar in t.pos]
            if pos_match:
                translations = pos_match

        if match_kana:
            # if word is only kana, find definition that is usually written in kana
            if is_hiragana(token.word) or is_katakana(token.word):
                kana_match = [t for t in translations if Grammar.USUALLY_KANA in t.misc]
            else:
                kana_match = [t for t in translations if Grammar.USUALLY_KANA not in t.misc]
            if kana_match:
                translations = kana_match

        translations.sort(key=lambda t: t.priority)
    return translations


def get_proper_noun(word):
    dictionary = Dictionary.get_dict().pn_dictionary
    return dictionary.get(word)
