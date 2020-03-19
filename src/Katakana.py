import pykakasi


def translate(jp):
    kakasi = pykakasi.kakasi()
    kakasi.setMode("K", "a")
    kakasi.setMode("r", "Hepburn")
    converter = kakasi.getConverter()
    hepburn = converter.do(jp)

    for i in range(len(hepburn)):
        try:
            current = hepburn[i]
            next_ = hepburn[i+1]
            if current == next_:
                hepburn = merge(i,hepburn)
        except IndexError:
            pass

    return hepburn


def merge(i, word: str):
    word_start = word[:i]
    word_end = word[i+2:]
    return word_start + convert_long_vowel(word[i]) + word_end


def convert_long_vowel(vowel):
    return {
        "a": "ā",
        "e": "ē",
        "i": "ī",
        "o": "ō",
        "u": "ū",
        "y": "ȳ"
    }.get(vowel)

