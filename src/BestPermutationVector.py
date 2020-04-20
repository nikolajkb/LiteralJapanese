import Constants
import BestPermutationFinder


class BestPermutationVector(BestPermutationFinder):
    def score(self,sentence):
        vectors = Constants.SIMILARITY.vectors
        total = 0
        for word in sentence:
            score = self.compare(word,sentence,vectors)
            total += score
        average = total / len(sentence)
        return average

    def compare(self,w1,sentence,vectors):
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
