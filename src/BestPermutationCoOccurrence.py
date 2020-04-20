import Constants
import BestPermutationFinder


class BestPermutationCoOccurrence(BestPermutationFinder):
    def score(self,permutation):
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
