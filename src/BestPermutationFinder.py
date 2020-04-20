from typing import List


class BestPermutationFinder:
    def best_combination(self,words: List[List[str]]):
        best_permutation = self.local_search(words)
        return best_permutation

    #  hillclimbing from the first words (most common) to a local maximum
    def local_search(self,words):
        current_best = [w[0] for w in words]
        max_score = self.score(current_best)
        neighbours = self.get_neighbours(current_best, words)
        while True:
            for neighbour in neighbours:
                score = self.score(neighbour)
                if score > max_score:
                    max_score = score
                    current_best = neighbour
                    neighbours = self.get_neighbours(current_best, words)
                    continue
            break
        print(max_score)
        return current_best

    def get_neighbours(self,configuration, words):
        neighbours = []
        i = 0
        for definitions in words:
            for word in definitions:
                neighbour = configuration.copy()
                neighbour[i] = word
                neighbours.append(neighbour)
            i += 1
        return neighbours

    def score(self, permutation):
        return NotImplementedError("Score should be implemented by a sub-class of BestPermutationFinder")
