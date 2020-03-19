import Tokenizer
import Infer
import LiteralJapanese
from Grammar import Grammar
from scripts import AlignCorpus
import nltk
from nltk.corpus import wordnet
import Katakana
import Numbers

q = Tokenizer.Token("ass", grammar=Grammar.UNKNOWN)
print(q)
