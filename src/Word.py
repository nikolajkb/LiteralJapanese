from typing import List


# specification
# writings: kanji and kana writings of the word, used as search key
# meanings: meanings of the word in English
# grammar: type of word; verb, noun etc.
class Word:
    def __init__(self, writings, meanings, grammar):
        self.writings: List[str] = writings
        self.meanings: List[str] = meanings


