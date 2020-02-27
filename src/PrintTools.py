def print_translated_sentence_alt(sentence, system, gold, score):
    print(" - sentence", sentence.index, " | score:", score, " - ")

    system_translation = ""
    system_tokens = ""
    gold_translation = ""
    original = ""
    max_len = max(len(gold), len(system))
    for i in range(max_len):
        try:
            system_t = system[i][1]
            system_t_o = system[i][0]
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

        add_system_o = system_t_o + spaces_jp(max_word_len, system_t_o)
        system_tokens += add_system_o

        add_system = system_t + spaces(max_word_len, system_t)
        system_translation += add_system

        add_gold = gold_t + spaces(max_word_len, gold_t)
        gold_translation += add_gold

        add_original = original_t + spaces_jp(max_word_len, original_t)
        original += add_original

    print(original)
    print(gold_translation)
    print(system_tokens)
    print(system_translation)


def spaces_jp(maxi, string): # TODO ? this is really dumb, the japanese letters are wider in the console than the english ones so I remove more spaces, this still does not work since there is a bit of float on longer sentences
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


def print_translated_sentence(sentence, system, gold):
    print(" - sentence", sentence.index, " - ")

    max_len = max(len(gold), len(system))
    for i in range(max_len):
        if i < len(gold):
            g = gold[i]
        else:
            g = SentenceToken("", "", "")
        if i < len(system):
            s = system[i]
        else:
            s = ("", "")

        print(g.japanese.ljust(8-len(g.japanese)), " ", g.english.ljust(30-len(g.english)), s[1])