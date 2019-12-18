import os
import xml.etree.ElementTree as ET


def parse():
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    file_name = os.path.join(file_dir, 'data', 'JMdict_e')
    tree = ET.parse(file_name)
    root = tree.getroot()
    i = 10
    for entry in root:
        k_ele_lst = entry.findall('k_ele')
        sense_lst = entry.findall('sense')
        if len(k_ele_lst) == 0 or len(sense_lst) == 0:
            continue
        i += 1
        print("Japanese:")
        for k_ele in k_ele_lst:
            keb_lst = k_ele.findall('keb')
            for keb in keb_lst:
                print(" "+keb.text)
        print("English:")
        for sense in sense_lst:
            gloss_lst = sense.findall('gloss')
            for gloss in gloss_lst:
                print(" "+gloss.text)
        print('-----------------------------------------')
        if i > 100:
            break


