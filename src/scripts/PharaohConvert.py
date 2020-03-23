def get_alignments():
    sentences = "/home/nikolaj/PycharmProjects/LitteralJapaneseTranslation/src/fast_align-master/sentences_dev.parallel"
    alignments = "/home/nikolaj/PycharmProjects/LitteralJapaneseTranslation/src/fast_align-master/sentences_dev.align"
    sentences_file = open(sentences,"r",encoding="utf-8")
    alignments_file = open(alignments,"r",encoding="utf-8")

    sentence_line = sentences_file.readline()
    alignment_line = alignments_file.readline()
    i = 1
    sentence_translations = {}
    while sentence_line:
        sentence_translation = {}
        jp_en = sentence_line.split(" ||| ")
        jp_tokens = jp_en[0].split(" ")
        en_tokens = jp_en[1][:-1].split(" ")

        align_split = alignment_line.split("|||")
        align_pairs = align_split[2].strip().split(" ")
        align_scores = align_split[4].strip().split(" ")

        align_pairs.sort(key=lambda p: japanese_index(p))

        print(jp_tokens)
        print(en_tokens)
        for pair in align_pairs:
            (i1,i2) = pair.split("-")
            (i1,i2) = (int(i1),int(i2))
            score = align_scores[i2]
            jp = jp_tokens[i1]
            en = en_tokens[i2]
            if sentence_translation.get(jp) is None:
                sentence_translation[jp] = en
            else:
                sentence_translation[jp] = sentence_translation[jp] + " " + en
            print(jp, "=", en + " ("+score+")", end=" | ")
        print("\n")

        sentence_translations[i] = sentence_translation
        i += 1
        sentence_line = sentences_file.readline()
        alignment_line = alignments_file.readline()

    return sentence_translations


def japanese_index(pair: str):
    pair = pair.split("-")
    return int(pair[0])
