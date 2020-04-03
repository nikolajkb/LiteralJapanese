import Equality
from colored import fg, attr

def write_to_file(system, file_path):
    file = open(file_path, "w+", encoding="utf-8")

    file.write("system tokens"+"\t"+"system translation"+"\n")
    for i in range(len(system)):
        try:
            system_translation = system[i].english
            system_token = system[i].japanese
        except IndexError:
            system_translation = ""
            system_token = ""

        file.write(system_token + "\t" + system_translation)
        if i != len(system):
            file.write("\n")


def print_translated_sentence_v(sentence, system, gold, score):
    print(" - sentence", sentence.index, " | score:", score, " - ")
    max_len = max(len(gold), len(system))
    for i in range(max_len):
        try:
            system_en = system[i].english
            system_jp = system[i].japanese
        except IndexError:
            system_en = ""
            system_jp = ""
        try:
            gold_en = gold[i].english
            gold_jp = gold[i].japanese
        except IndexError:
            gold_en = ""
            gold_jp = ""

        line = gold_jp + "\t" + gold_en + "\t" + system_jp + "\t" + system_en
        if len(gold) == len(system):
            if Equality.equals(system_en,gold_en):
                print(add_color(line,"green"))
            else:
                print(add_color(line,"red"))
        else:
            print(line)
    print("\n")


def print_translated_sentence(sentence, system, gold, score):
    print(" - sentence", sentence.index, " | score:", score, " - ")

    system_translation = ""
    system_tokens = ""
    gold_translation = ""
    original = ""
    max_len = max(len(gold), len(system))
    for i in range(max_len):
        try:
            system_t = system[i].english
            system_t_o = system[i].japanese
        except IndexError:
            system_t = ""
            system_t_o = ""
        try:
            gold_t = gold[i].english
            original_t = gold[i].japanese
        except IndexError:
            gold_t = ""
            original_t = ""
        max_word_len = len(max(system_t,gold_t,original_t, key=len))

        add_gold = gold_t + spaces(max_word_len, gold_t)
        gold_translation += add_gold

        add_original = original_t + spaces_jp(max_word_len, original_t)
        original += add_original

        add_system_o = system_t_o + spaces_jp(max_word_len, system_t_o)
        system_tokens += add_system_o

        add_system = system_t + spaces(max_word_len, system_t)
        system_translation += add_system

    print(original)
    print(gold_translation)
    print(system_tokens)
    print(system_translation)


def add_color(string, color):
    return fg(color) + string + attr("reset")


def spaces_jp(maxi, string):  # TODO ? this is really dumb, the japanese letters are wider in the console than the english ones so I remove more spaces, this still does not work since there is a bit of float on longer sentences
    maxi += 10
    ret = ""
    strlen = len(string) * 1.75
    strlen = round(strlen)
    for i in range(maxi - strlen):
        ret += " "
    return ret


def spaces(maxi, string):
    maxi += 10
    ret = ""
    for i in range(maxi - len(string)):
        ret += " "
    return ret

