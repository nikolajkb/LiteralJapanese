import os
import xml.etree.ElementTree as ET

file_dir = os.path.dirname(os.path.realpath('__file__'))
file_name = os.path.join(file_dir, '..', 'data', 'JMdict_e')
tree = ET.parse(file_name)
root = tree.getroot()
file_dir = os.path.dirname(os.path.realpath('__file__'))
file_name = os.path.join(file_dir, '..', "user_dict.csv")
file_handler = open(file_name, "w")
for entry in root:
    writings = []
    readings = []
    pos = []
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

    for misc in sense.findall("misc"):
        word.misc.append(make_grammar(misc.text))

    file_handler.write()