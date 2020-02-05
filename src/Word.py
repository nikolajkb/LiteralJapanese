from typing import List
from Grammar import Grammar


# specification
# writings: kanji and kana writings of the word, used as search key
# meanings: meanings of the word in English
# pos: part of speech type of word; verb, noun etc.
class Word:
    def __init__(self, writings, meanings, pos):
        self.writings: List[str] = writings
        self.meanings: List[str] = meanings
        self.pos: List[Grammar] = pos


def make_empty():
    return Word([], [], [])
