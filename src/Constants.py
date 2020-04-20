import os
from sudachipy import dictionary as sudachi_dict

VERBOSE = False
PARAPHRASE = False
WEIGHTED_SIMILARITY = False
TOKENIZER = sudachi_dict.Dictionary().create()
PROJECT_DIR = os.path.dirname(os.path.realpath('__file__'))
SIMILARITY = None
WIKI_STATS = None
