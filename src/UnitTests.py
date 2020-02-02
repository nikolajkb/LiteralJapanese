import unittest
import Tokenizer
import WordEndingTranslator


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


class EndingsTest(unittest.TestCase):
    def test_endings_1(self):
        tokens = [Tokenizer.Token("ま",None,None,None),Tokenizer.Token("せんでし",None,None,None),Tokenizer.Token("た",None,None,None)]
        self.assertEqual([WordEndingTranslator.Ending.POLITE,WordEndingTranslator.Ending.NEGATIVE,WordEndingTranslator.Ending.PAST],WordEndingTranslator.translate_ending(tokens))


if __name__ == '__main__':
    unittest.main()
