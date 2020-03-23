import os

from gensim.models import KeyedVectors
from gensim.test.utils import datapath
from gensim.parsing.preprocessing import remove_stopwords
import Constants
import re


class Similarity:
    def __init__(self):
        print("loading word vectors")
        self.vectors = self._load_vectors()

    def is_similar(self, s1: str, s2: str):
        return self.similarity(s1,s2) > 0.4

    def similarity(self, s1: str,s2: str):
        if self._is_valid_expression(s1) and self._is_valid_expression(s2):
            if len(s1) == 1 and len(s2) == 1:
                return self._word_similarity(s1,s2)
            else:
                return self._expression_similarity(s1,s2)
        else:
            return 0

    def _word_similarity(self,s1,s2):
        return self.vectors.similarity(s1,s2)

    def _expression_similarity(self,e1,e2):
        e1 = self._remove_stopwords(e1).split()
        e2 = self._remove_stopwords(e2).split()
        if self._either_empty(e1,e2):
            return 0  # TODO
        try:
            return self.vectors.n_similarity(e1,e2)
        except KeyError:
            return 0  # one or more words are not in vocab

    def _either_empty(self,l1,l2):
        return len(l1) == 0 or len(l2) == 0

    def _remove_stopwords(self, s):
        return remove_stopwords(s)

    def _is_valid_expression(self, s):
        # match anything that consists of numbers and letters, possibly with spaces around them
        return re.match("^(?: *[a-zA-Z0-9]+ *)*$",s)

    def _load_vectors(self):
        file_dir = Constants.project_dir
        file_path = os.path.join(file_dir,"..","data","GoogleNewsVectors","GoogleNews-vectors-negative300.bin")
        return KeyedVectors.load_word2vec_format(datapath(file_path), binary=True, limit=1_000_000)
