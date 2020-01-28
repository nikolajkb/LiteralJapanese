from src import Tokenizer, Dict_translator
import Tests


def translate(text):
    tokens = Tokenizer.get_tokens(text)
    translations = Dict_translator.translate(tokens)
    return translations


Tokenizer.get_tokens("残ったものはなにひとつありませんでした。 ")
Tokenizer.get_tokens("日曜日に出社したので月曜日が代休だった")
Tokenizer.get_tokens("彼女は登校前によく髪を洗ったものだった。")
Tokenizer.get_tokens("七夕は漫画によく出てくるので、私もそこそこ知っています。")
Tokenizer.get_tokens("七夕は#漫画によく出てくるので、私もそこそこ知っています。")

Tests.read_test_data()






