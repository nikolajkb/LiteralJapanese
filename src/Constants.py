import os
from sudachipy import dictionary as sudachi_dict

VERBOSE = False
PARAPHRASE = False
WEIGHTED_SIMILARITY = True
tokenizer = sudachi_dict.Dictionary().create()
project_dir = os.path.dirname(os.path.realpath('__file__'))
similarity = None
