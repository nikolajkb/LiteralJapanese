import Tokenizer
import Infer
import LiteralJapanese
from scripts import AlignCorpus

AlignCorpus.from_ud_pud()
#tokens = Tokenizer.get_tokens("会長が個人的に私の手紙に返事をくれるとは思いもよらなかった。")
#infer = Infer.infer(tokens,"I didn't imagine the chairman would reply to my letter in person.")
#translated = LiteralJapanese.translate("会長が個人的に私の手紙に返事をくれるとは思いもよらなかった。")

print("stop")
