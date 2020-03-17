import Tokenizer
import Infer
import LiteralJapanese
from scripts import AlignCorpus

tokens = Tokenizer.get_tokens("三日前は残念なことにマグニチュード8.9の地震が日本の東北地方太平洋沖で発生した")
infer = Infer.infer(tokens,"Unfortunately, three days ago a magnitude 8.8 earthquake struck off the Pacific coast of Japan's Tohoku region.")
translated = LiteralJapanese.translate("三日前は残念なことにマグニチュード8.9の地震が日本の東北地方太平洋沖で発生した。")

print("stop")
