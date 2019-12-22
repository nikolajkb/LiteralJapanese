import nagisa
from sudachipy import tokenizer
from sudachipy import dictionary
from src import XmlReader, Tokenizer

Tokenizer.get_tokens("家を出ようとしたら、トムが私に電話してきた。")
Tokenizer.get_tokens("日曜日に出社したので月曜日が代休だった")

tokenizer_obj = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.C
print([m.surface() for m in tokenizer_obj.tokenize("日曜日に出社したので月曜日が代休だった", mode)])
print([m.surface() for m in tokenizer_obj.tokenize("家を出ようとしたら、トムが私に電話してきた。", mode)])




