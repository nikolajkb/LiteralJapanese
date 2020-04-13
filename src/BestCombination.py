import WikiMatrix
from typing import List
import itertools

stats = WikiMatrix.load_matrix()


def best_combination(words: List[List[str]]):
    permutations = list(itertools.product(*words))
    max_score = -1
    best_permutation = None
    for permutation in permutations:
        total = 0
        for w1 in permutation:
            for w2 in permutation:
                if w1 != w2:
                    if stats.frequencies.get(w1) is None or stats.frequencies.get(w2) is None:
                        continue
                    else:
                        score = stats.matrix[w1][w2]
                        score = score / stats.frequencies.get(w1)
                        total += score
        total = total/len(permutation)
        print(permutation,total)
        if total > max_score:
            best_permutation = permutation
            max_score = total
    return best_permutation
