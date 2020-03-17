sentences = "/home/nikolaj/PycharmProjects/LitteralJapaneseTranslation/src/fast_align-master/build/sentences_dev.align"
alignments = "/home/nikolaj/PycharmProjects/LitteralJapaneseTranslation/src/fast_align-master/build/sentences_dev.gdfa"
sentences_file = open(sentences,"r",encoding="utf-8")
alignments_file = open(alignments,"r",encoding="utf-8")

sentence_line = sentences_file.readline()
alignment_line = alignments_file.readline()
i = 0
while sentence_line:
    jp_en = sentence_line.split(" ||| ")
    jp_tokens = jp_en[0].split(" ")
    en_tokens = jp_en[1].split(" ")
    align_pairs = alignment_line.split(" ")

    print(jp_tokens)
    print(en_tokens)
    for pair in align_pairs:
        (i1,i2) = pair.split("-")
        (i1,i2) = (int(i1),int(i2))
        print(jp_tokens[i1], "=", en_tokens[i2], end=" | ")
    print("\n")

    i += 1
    if i > 10:
        break
    sentence_line = sentences_file.readline()
    alignment_line = alignments_file.readline()

