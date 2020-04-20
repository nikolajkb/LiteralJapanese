import Constants
import Paraphrase


def equals(source, target):
    if source == target:
        return True
    if Constants.PARAPHRASE and not_small_words(source,target):
        return is_paraphrase(source,target) or is_similar(source,target) or is_substring(source,target)
    else:
        return False


# only used for testing purposes
def equals_rule(source, target):
    if source == target:
        return True,"strict equality"
    if not_small_words(source,target):
        if is_paraphrase(source,target):
            return True,"is paraphrase"
        elif is_substring(source,target):
            return True,"is substring"
        elif is_similar(source,target):
            return True,"vector is similar"

    return False, "not equal"


def not_small_words(source,length):
    return len(source) > 2 and len(length) > 2


def is_paraphrase(source, target):
    paraphrases = Paraphrase.Ppdb.get_ppdb()
    similar = paraphrases.get(target, [])
    return source in similar


def is_substring(source: str,target: str):
    return (target in source or source in target) and \
           ("-" not in source and "-" not in target)  # '-' is used to represent inflections of words. Not filtering this
                                                      # would result in false positives like: -polite-past = -past


def is_similar(source,target):
    return Constants.SIMILARITY.is_similar(source, target)
