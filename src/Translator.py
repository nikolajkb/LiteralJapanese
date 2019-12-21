import nagisa
from src import XmlReader, Tokenizer

XmlReader.parse()
text = 'ただし、50周年ソングに変更後は、EDも歌つきのものが使われた'
words = nagisa.tagging(text)
print(words)

