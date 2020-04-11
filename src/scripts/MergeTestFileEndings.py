from typing import List

from Tests import SentenceToken, read_test_data
import os


def convert():
    sentences = read_test_data(r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\sentences_dev.txt")
    sentences = merge_word_endings(sentences)

    new_file_path = r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\sentences_dev_m.txt"
    new_file = open(new_file_path,"w+", encoding="utf-8")
    for sentence in sentences:
        new_file.write("#"+str(sentence.index)+"\n")
        new_file.write("#jp\t"+sentence.japanese+"\n")
        new_file.write("#en\t"+sentence.english+"\n")
        for sentencetoken in sentence.tokens:
            jp = sentencetoken.japanese
            en = sentencetoken.english
            if sentencetoken.japanese == " ":
                jp = "\space"
            if sentencetoken.english == " ":
                en = "\space"
            new_file.write(jp+"\t"+en+"\n")
        new_file.write("\n")


def merge_word_endings(sentences):
    for sentence in sentences:
        sentence.tokens = merge_token_list(sentence.tokens)

    return sentences


def merge_token_list(tokens: List[SentenceToken]):
    merged = []
    i = 0
    while i < len(tokens):
        if is_ending(tokens[i]):
            ending = tokens[i]
            i += 1
            while i < len(tokens) and is_ending(tokens[i]):
                ending = merge_tokens(ending, tokens[i])
                i += 1
            merged.append(ending)
            i -= 1
        elif not is_ending(tokens[i]):
            merged.append(tokens[i])
        i += 1

    return merged


def is_ending(token):
    return token.english.startswith("-")


def merge_tokens(t1, t2):
    (min_i, _) = t1.indices
    (_, max_i) = t2.indices
    return SentenceToken(t1.japanese + t2.japanese, t1.english + t2.english, (min_i, max_i))