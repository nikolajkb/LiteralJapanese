import Constants
from typing import List


def best_combination(words: List[List[str]]):
    best_permutation = local_search(words)
    return best_permutation


#  hillclimbing from the first words (most common) to a local maximum
def local_search(words):
    current_best = [w[0] for w in words]
    max_score = co_score(current_best)
    neighbours = get_neighbours(current_best,words)
    while True:
        for neighbour in neighbours:
            score = co_score(neighbour)
            if score > max_score:
                max_score = score
                current_best = neighbour
                neighbours = get_neighbours(current_best,words)
                continue
        break
    return current_best


def get_neighbours(configuration, words):
    neighbours = []
    i = 0
    for definitions in words:
        for word in definitions:
            neighbour = configuration.copy()
            neighbour[i] = word
            neighbours.append(neighbour)
        i += 1
    return neighbours


def co_score(sentence):
    vectors = Constants.SIMILARITY.vectors
    total = 0
    for word in sentence:
        score = compare(word,sentence,vectors)
        total += score
    average = total / len(sentence)
    return average


def compare(w1,sentence,vectors):
    total = 0
    for w2 in sentence:
        try:
            similarity = vectors.similarity(w1,w2)
            total += similarity
        except KeyError:
            try:
                if w1 == " " or w2 == " ":
                    continue
                similarity = vectors.n_similarity(w1.split(),w2.split())
                total += similarity
            except KeyError:
                pass
    return total / len(sentence)
