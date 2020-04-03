import LiteralJapanese
import Tests
from Similarity import init_similarity
import Dictionary
import Equality
import Translator
from Grammar import Grammar

sentences = Tests.read_test_data(r"C:\Users\Nikolaj\PycharmProjects\LitteralJapaneseTranslation\data\sentences_dev.txt")
init_similarity()
wrong_def = 0
wrong_word = 0
particle_error = 0
other = 0

for sentence in sentences:
    system = LiteralJapanese.translate(sentence.japanese, translation=sentence.english)
    gold = sentence.tokens
    min_len = min(len(system),len(gold))
    for i in range(min_len-1):
        s_token = system[i]
        g_token = gold[i]
        if s_token.japanese == g_token.japanese:
            is_particle = False
            if s_token.token.grammar == Grammar.PARTICLE:
                is_particle = True

            if not Equality.equals(g_token.english,s_token.english) and g_token.japanese == s_token.japanese:
                if is_particle:
                    particle_error += 1
                    continue
                entries = Dictionary.get(s_token.token.root)
                equality_found = False
                for entry in entries:
                    is_chosen_word = False
                    if Translator.clean_word(entry.meanings[0]) == s_token.english:
                        is_chosen_word = True
                    else:
                        stophere = 1

                    if any([Translator.clean_word(m) == g_token.english for m in entry.meanings]):
                        if is_chosen_word:
                            wrong_def += 1
                            equality_found = True
                        else:
                            wrong_word += 1
                            equality_found = True
                        break
                if not equality_found:
                    other += 1

print("wrong definition", wrong_def)
print("wrong word      ", wrong_word)
print("particle        ", particle_error)
print("other           ", other)
