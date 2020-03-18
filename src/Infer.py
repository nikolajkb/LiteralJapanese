import Dictionary
import Translator
import nltk
from Grammar import Grammar


# args are tokenized japanese and un-tokenized english
def infer(source,target):
    target = [t.lower() for t in nltk.tokenize.word_tokenize(target)]
    inferred_translations = {}
    for token in source:
        inferred_translation = ""

        translations = get_all_meanings(token)

        for translation in translations:
            if translation in target:
                inferred_translation = translation
                target.remove(translation)
                break

        if inferred_translation != "":
            inferred_translations[token.word] = inferred_translation

    return inferred_translations


def get_all_meanings(token):
    entries = Dictionary.match(token)
    if entries is None:
        return []
    translations = []
    for entry in entries:
        translations.extend(entry.meanings)
    translations = [Translator.clean_word(t).strip().lower() for t in translations]
    return translations
