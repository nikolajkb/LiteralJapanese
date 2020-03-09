import os
import xml.etree.ElementTree as ET
import re

import Grammar


def read_pn_dictionary():

    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, '..', "data", "katakana.txt")
    katakana = open(file_name, "w", encoding="utf-8")

    file_name = os.path.join(file_dir, '..', 'data', 'JMnedict.xml')
    tree = ET.parse(file_name)
    root = tree.getroot()
    parse_pn_dict(root,katakana)

    file_name = os.path.join(file_dir, '..', 'data', 'JMnedict_2.xml')
    tree = ET.parse(file_name)
    root = tree.getroot()
    parse_pn_dict(root,katakana)


def parse_pn_dict(root, file):

    for entry in root:
        katakana = ""
        translation = ""

        r_ele = entry.find("r_ele")
        if r_ele is not None:
            reb = r_ele.find("reb")
            katakana = reb.text

        trans = entry.find("trans")
        if trans is not None:
            trans_det = trans.find("trans_det")
            if trans_det is not None:
                translation = trans_det.text

        translation = re.sub(" ?\(.*\)", "", translation)

        if not Grammar.is_katakana(katakana):
            continue
        if translation == "":
            continue
        if len(translation) > 12:
            continue
        if translation.find(" ") != -1:
            continue

        file.write(katakana + "\t" + translation + "\n")


read_pn_dictionary()
