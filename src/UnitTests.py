import unittest
import Tokenizer


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


if __name__ == '__main__':
    unittest.main()
