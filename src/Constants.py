import os
from sudachipy import dictionary as sudachi_dict

VERBOSE = False
PARAPHRASE = False
tokenizer = sudachi_dict.Dictionary().create()
project_dir = os.path.dirname(os.path.realpath('__file__'))
similarity = None
