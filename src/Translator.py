from src import XmlReader, Tokenizer

XmlReader.parse()

words = Tokenizer.get_tokens("hello")
error = Tokenizer._tokenize()


