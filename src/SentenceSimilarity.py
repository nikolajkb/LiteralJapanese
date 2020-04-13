import Constants
import Similarity
from statistics import mean
from typing import List
import itertools


def best_combination(words: List[List[str]]):
    permutations = list(itertools.product(*words))
    return get_most_probable(permutations)


def get_most_probable(sentences):
    max_score = 99
    best_sentence = None
    for sentence in sentences:
        score = co_score(sentence)
        if score < max_score:
            max_score = score
            best_sentence = sentence
    return best_sentence


def co_score(sentence):
    vectors = Constants.SIMILARITY.vectors
    total = 0
    for word in sentence:
        similarity = vectors.distances(word,sentence)
        total += mean(similarity)
    average = total / len(sentence)
    return average
