from scripts import PharaohConvert
from src import Constants
import Tests
import PrintTools

convert = PharaohConvert.get_alignments()
sentences = Tests.read_test_data(r"/home/nikolaj/PycharmProjects/LitteralJapaneseTranslation/data/sentences_dev.txt")
sentences = Tests.merge_word_endings(sentences)
scores = []

i = 1
for sentence in sentences:
    system = [(k, v) for k, v in convert.get(i).items()]
    gold = sentence.tokens
    score = Tests.translation_sentence_score(gold, system)
    PrintTools.print_translated_sentence(sentence, system, gold, score)
    scores.append(Tests.TranslationScore(len(gold), score))
    i += 1


avg = Tests.TranslationScore.make_average(scores)
print("#### average result (Levenshtein distance) ####")
avg.print()
