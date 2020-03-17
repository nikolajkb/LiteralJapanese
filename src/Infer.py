import Dictionary
import Translator
import nltk


# args are tokenized japanese and un-tokenized english
def infer(source,target):
    target = nltk.tokenize.word_tokenize(target)
    inferred_translations = []
    for token in source:
        inferred_translation = ""
        entries = Dictionary.match(token)
        if entries is None:
            inferred_translations.append((token.word, "NO TRANSLATION"))
            continue
        translations = []
        for entry in entries:
            translations.extend(entry.meanings)

        translations = [Translator.clean_word(t).strip() for t in translations]
        for translation in translations:
            if translation in target:
                inferred_translation = translation
                break
        if inferred_translation == "":
            inferred_translations.append((token.word,"NO TRANSLATION"))
        else:
            inferred_translations.append((token.word,inferred_translation))
    print(source)
    print(target)
    print(inferred_translations)
    return inferred_translations
