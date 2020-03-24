import pykakasi


# translates a Japanese name to the English translation using hepburn conversion with macrons indicating long vowels
def translate(name):
    kakasi = pykakasi.kakasi()
    kakasi.setMode("J","a")
    kakasi.setMode("r", "Hepburn")
    converter = kakasi.getConverter()
    hepburn = converter.do(name)
    hepburn = add_long_vowel_lines(hepburn)
    return hepburn


def add_long_vowel_lines(hepburn):
    for i in range(len(hepburn)):
        try:
            current = hepburn[i]
            next_ = hepburn[i+1]
            if current == next_ and is_vowel(current):
                hepburn = merge(i,hepburn)
        except IndexError:
            pass
    return hepburn


def merge(i, word: str):
    word_start = word[:i]
    word_end = word[i+2:]
    return word_start + convert_long_vowel(word[i]) + word_end


# y is not included since it does not exist in Japanese
def is_vowel(letter):
    return letter in "aeiou"


def convert_long_vowel(vowel):
    return {
        "a": "ā",
        "e": "ē",
        "i": "ī",
        "o": "ō",
        "u": "ū",
    }.get(vowel)
