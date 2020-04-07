# Warning: these test cases cover only selected functions. The built-in test functionality
#          should be used for regression testing

import unittest
import Numbers
import Translator
import Tokenizer
import Grammar


class TokenTests(unittest.TestCase):
    def test_token_word(self):
        tokens = Tokenizer.get_tokens("残ったものはなにひとつありませんでした。 ")
        self.assertEqual("残っ", tokens[0].word)

    def test_token_indices(self):
        tokens = Tokenizer.get_tokens("残ったものはなにひとつありませんでした。 ")
        self.assertEqual([0, 2], tokens[0].char_indices)

    def test_token_grammar(self):
        tokens = Tokenizer.get_tokens("残ったものはなにひとつありませんでした。 ")
        self.assertEqual(Tokenizer.Grammar.VERB, tokens[0].grammar)

    def test_token_root(self):
        tokens = Tokenizer.get_tokens("残ったものはなにひとつありませんでした。 ")
        self.assertEqual("残る", tokens[0].root)

    def test_token_merging(self):
        tokens = Tokenizer.get_tokens("食べたくなかった")
        self.assertEqual([0,2],tokens[0].char_indices)
        self.assertEqual([2,8],tokens[1].char_indices)


class GrammarTests(unittest.TestCase):
    def test_kana(self):
        self.assertEqual(Grammar.is_hiragana("いいえ"), True)
        self.assertEqual(Grammar.is_hiragana("ない"), True)
        self.assertEqual(Grammar.is_hiragana("ばば"), True)
        self.assertEqual(Grammar.is_hiragana("ぱ"), True)

        self.assertEqual(Grammar.is_hiragana("渡辺"), False)
        self.assertEqual(Grammar.is_hiragana("以上"), False)
        self.assertEqual(Grammar.is_hiragana("いつもお世話になっております。"), False)
        self.assertEqual(Grammar.is_hiragana("昔の"), False)

        self.assertEqual(Grammar.is_hiragana("きゅう"), True)
        self.assertEqual(Grammar.is_hiragana("にゃん"), True)
        self.assertEqual(Grammar.is_hiragana("やっぱり"), True)

    def test_is_english(self):
        self.assertEqual(True, Grammar.is_english("2004"))
        self.assertEqual(True, Grammar.is_english("2.4"))
        self.assertEqual(True, Grammar.is_english("2,4"))

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


class ParenthesesTests(unittest.TestCase):
    def test_parentheses_1(self):
        word = "this (something or someone close to the speaker (including the speaker), or ideas expressed by the speaker)"
        reduced = Translator.remove_parentheses(word)
        self.assertEqual("this",reduced.strip())

    def test_parentheses_2(self):
        word = "this (something or someone close to the speaker)"
        reduced = Translator.remove_parentheses(word)
        self.assertEqual("this",reduced.strip())

    def test_parentheses_3(self):
        word = "(not) either (in a negative sentence)"
        reduced = Translator.remove_parentheses(word)
        self.assertEqual("either",reduced.strip())

    def test_parentheses_4(self):
        word = "(not) either"
        reduced = Translator.remove_parentheses(word)
        self.assertEqual("either",reduced.strip())


if __name__ == '__main__':
    unittest.main()
