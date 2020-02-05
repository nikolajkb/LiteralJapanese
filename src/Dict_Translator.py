from XmlReader import XmlReader
import Word


def translate(tokens):
    dicti = XmlReader().get_dict()
    translation = []
    for token in tokens:
        eng = dicti.get(token.root)
        if eng is None:
            eng = Word.make_empty()
            eng.meanings.append("ERROR")
        jp = token.word
        translation.append((jp, eng.meanings[0]))

    return translation
