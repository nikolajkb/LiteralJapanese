from Grammar import Grammar


def make_grammar(tag):
    {
        "CC": Grammar.CONJUNCTION,
        "CD": Grammar.NUMBER,
        "SYM": Grammar.SYMBOL,
        "NN": Grammar.NOUN,
        "NNP": Grammar.PROPER_NOUN,
        "XS": Grammar.MOD_NOUN,
        "XSC": Grammar.COUNTER,
        "PS": Grammar.PARTICLE,
        "PN": Grammar.PARTICLE_NO,
        "PC": Grammar.PARTICLE_CONJ,
        "PH": Grammar.PARTICLE,
        "PK": Grammar.PARTICLE,
        "JJ": Grammar.I_ADJECTIVE,
        "JN": Grammar.NA_ADJECTIVE,
        "JR": Grammar.DETERMINER,
        "AV": Grammar.ENDING,
        "XV": Grammar.AUX_VERB,
        "VV": Grammar.VERB,
        "PQ": Grammar.PARTICLE_QUOTE,
        "UH": Grammar.INTERJECTION
    }.get(tag, Grammar.UNKNOWN)
