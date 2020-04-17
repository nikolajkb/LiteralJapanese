import Constants
import WikiMatrix
from typing import List


def best_combination(words: List[List[str]]):
    best_permutation = local_search(words)
    return best_permutation


#  hillclimbing from the first words (most common) to a local maximum
def local_search(words):
    current_best = [w[0] for w in words]
    max_score = permutation_score(current_best)
    neighbours = get_neighbours(current_best,words)
    while True:
        for neighbour in neighbours:
            score = permutation_score(neighbour)
            if score > max_score:
                max_score = score
                current_best = neighbour
                neighbours = get_neighbours(current_best,words)
                continue
        break
    print(max_score)
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


def permutation_score(permutation):
    total = 0
    for w1 in permutation:
        for w2 in permutation:
            if w1 != w2:
                if Constants.WIKI_STATS.frequencies.get(w1) is None or Constants.WIKI_STATS.frequencies.get(w2) is None:
                    continue
                else:
                    score = Constants.WIKI_STATS.matrix[w1][w2]
                    score = score / Constants.WIKI_STATS.frequencies.get(w1)
                    total += score
    return total / len(permutation)  # not really necessary since all permutations are same length, but enables comparing of sentences of differing lengths
