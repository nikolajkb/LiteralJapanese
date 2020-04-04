from typing import List
from Grammar import Grammar


# specification
# writings: kanji and kana writings of the word, used as search key
# meanings: meanings of the word in English
# pos: part of speech type of word; verb, noun etc.
# priority: priority of the word i.e. how common it is.
class Word:
    def __init__(self, writings, meanings, pos, misc=None, priority=99999):
        if misc is None:
            misc = []
        self.writings: List[str] = writings
        self.meanings: List[str] = meanings
        self.pos: List[Grammar] = pos
        self.misc: List[Grammar] = misc
        self.priority = priority


def make_empty():
    return Word([], [], [])


def copy(word):
    return Word(word.writings.copy(),word.meanings.copy(),word.pos.copy(),word.misc.copy(),word.priority)
