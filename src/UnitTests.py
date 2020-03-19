import os
import unittest

import Numbers
import Translator
import Tokenizer
import LiteralJapanese
from Grammar import Grammar
from Grammar import is_hiragana
import Grammar
import PrintTools


class TokenTests(unittest.TestCase):
    def test_token_word(self):
        tokens = Tokenizer.get_tokens("残ったものはなにひとつありませんでした。 ")
        self.assertEqual("残っ", tokens[0].word)

    def test_token_indices(self):
        tokens = Tokenizer.get_tokens("残ったものはなにひとつありませんでした。 ")
        self.assertEqual((0, 2), tokens[0].char_indices)

    def test_token_grammar(self):
        tokens = Tokenizer.get_tokens("残ったものはなにひとつありませんでした。 ")
        self.assertEqual(Tokenizer.Grammar.VERB, tokens[0].grammar)

    def test_token_root(self):
        tokens = Tokenizer.get_tokens("残ったものはなにひとつありませんでした。 ")
        self.assertEqual("残る", tokens[0].root)

    def test_token_merging(self):
        tokens = Tokenizer.get_tokens("食べたくなかった")
        self.assertEqual((0,2),tokens[0].char_indices)
        self.assertEqual((2,6),tokens[1].char_indices)


class EndingTranslatorTests(unittest.TestCase):
    def test_ending_0(self):
        token = Tokenizer.Token("ませんでした", Grammar.MERGED, "", (1, 1))
        translation = Translator.translate_ending(token)
        self.assertEqual(translation,"-polite-negative-past")

    def test_ending_1(self):
        token = Tokenizer.Token("ちゃった", Grammar.MERGED, "", (1, 1))
        translation = Translator.translate_ending(token)
        self.assertEqual(translation, "-unintentional-past")

    def test_ending_2(self):
        token = Tokenizer.Token("させられない", Grammar.MERGED, "", (1, 1))
        translation = Translator.translate_ending(token)
        self.assertEqual(translation, "-causative-passive-negative")

    def test_ending_3(self):
        token = Tokenizer.Token("ていない", Grammar.MERGED, "", (1, 1))
        translation = Translator.translate_ending(token)
        self.assertEqual(translation, "-ongoing-negative")

    def test_ending_4(self):
        token = Tokenizer.Token("れて", Grammar.MERGED, "", (1, 1))
        translation = Translator.translate_ending(token)
        self.assertEqual(translation, "-passive-te")

    def test_ending_5(self):
        token = Tokenizer.Token("じゃなかった", Grammar.MERGED, "", (1, 1))
        translation = Translator.translate_ending(token)
        self.assertEqual(translation, "-negative-past")


class GrammarTests(unittest.TestCase):
    def test_kana(self):
        self.assertEqual(is_hiragana("いいえ"), True)
        self.assertEqual(is_hiragana("ない"), True)
        self.assertEqual(is_hiragana("ばば"), True)
        self.assertEqual(is_hiragana("ぱ"), True)

        self.assertEqual(is_hiragana("渡辺"), False)
        self.assertEqual(is_hiragana("以上"), False)
        self.assertEqual(is_hiragana("いつもお世話になっております。"), False)
        self.assertEqual(is_hiragana("昔の"), False)

        self.assertEqual(is_hiragana("きゅう"), True)
        self.assertEqual(is_hiragana("にゃん"), True)
        self.assertEqual(is_hiragana("やっぱり"), True)

    def test_is_english(self):
        self.assertEqual(True, Grammar.is_english("2004"))
        self.assertEqual(True, Grammar.is_english("2.4"))
        self.assertEqual(True, Grammar.is_english("2,4"))


class PrintTests(unittest.TestCase):
    def test_write(self):
        text = "system tokens" + "\t" + "system translation" + "\n"

        file_name = "test_write"
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        file_name = os.path.join(file_dir, '..', "data", file_name)

        translation = LiteralJapanese.translate("残ったものはなにひとつありませんでした")

        PrintTools.write_to_file(translation,file_name)

        file = open(file_name,"r",encoding="utf-8")
        self.assertEqual(text,file.readline())


class NumberTests(unittest.TestCase):
    def test_number_1(self):
        number = "１２３８３万"
        english = Numbers.convert(number)
        self.assertEqual("123.83 million",english)

    def test_number_2(self):
        number = "三一一"
        english = Numbers.convert(number)
        self.assertEqual("311",english)

    def test_number_3(self):
        number = "二〇〇"
        english = Numbers.convert(number)
        self.assertEqual("200",english)

    def test_number_4(self):
        number = "90億"
        english = Numbers.convert(number)
        self.assertEqual("9 billion",english)


if __name__ == '__main__':
    unittest.main()
