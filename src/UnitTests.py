import unittest

import Dict_Translator
import Tokenizer
from Grammar import Grammar
from Grammar import is_hiragana


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


class EndingTranslatorTests(unittest.TestCase):
    def test_ending_0(self):
        token = Tokenizer.Token("ませんでした", Grammar.MERGED, "", (1, 1))
        translation = Dict_Translator.translate_ending(token)
        self.assertEqual(translation,"-polite-negative-past")

    def test_ending_1(self):
        token = Tokenizer.Token("ちゃった", Grammar.MERGED, "", (1, 1))
        translation = Dict_Translator.translate_ending(token)
        self.assertEqual(translation, "-unintentional-past")

    def test_ending_2(self):
        token = Tokenizer.Token("させられない", Grammar.MERGED, "", (1, 1))
        translation = Dict_Translator.translate_ending(token)
        self.assertEqual(translation, "-causative-passive-negative")

    def test_ending_3(self):
        token = Tokenizer.Token("ていない", Grammar.MERGED, "", (1, 1))
        translation = Dict_Translator.translate_ending(token)
        self.assertEqual(translation, "-ongoing-negative")


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

if __name__ == '__main__':
    unittest.main()
