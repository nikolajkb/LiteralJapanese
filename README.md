# Literal Japanese Translation
**Note: this system was created as a Bachelor's project and should not be viewed as a production ready library**
#### About
Literal Japanese is a Japanese-English translator that translates word by word and thus preserves Japanese grammar. 
Literal Japanese is intended as a tool for Japanese learners who want to learn about Japanese sentence structure.
#### Installation
1. run setup.py
2. install sudachipy dictionary\
pip install https://object-storage.tyo2.conoha.io/v1/nc_2520839e1f9641b08211a5c85243124a/sudachi/SudachiDict_core-20191224.tar.gz
3. run LiteralJapanese.py\
use -h argument to display available commands

#### Translating
Translations can be done interactively in the command line:\
`LiteralJapanese.py --interactive`\
A translations can also be saved to a specified file:\
`--translate "勉強すればするほど分かる。" "translation.txt"`\
This will write the translated tokens one line at a time\
A file containing one or more sentences can also be specified:\
`--translate --batch "input.txt" "output.txt"`
##### Using python
Translations can be done programmatically by calling the `translate(text)` function located in LiteralJapanese.py.
This will return a list of Translation objects that have three attributes.
1. ``japanese`` (the Japanese token)
2. ``english`` (the English translation of the token)
3. ``token`` (a token object with info on POS etc., refer to Tokenizer.py)

#### Testing
To test the system, you need to provide a test file. Two test files are provided in the data folder.\
Example command:\
`LiteralJapanese.py --test "...LiteralJapaneseTranslation\data\sentences_dev.txt" -v` \
You can also test only the tokenization using the --tt command\
\
The system can count translations as correct if they are synonyms of the gold translation using the ``-p`` argument. 
This requires two additional files.
1. Google news vectors  
https://code.google.com/archive/p/word2vec/ \
must be located in ``data/GoogleNewsVectors/GoogleNews-vectors-negative300.bin``
2. Paraphrase database \
http://paraphrase.org/#/download (small version) \
must be located in `data/PPDB/ppdb-2.0-s-all`

##### Test file format
A test file consists of Sentences. For each sentence can have four elements.
1. A numeric id for the sentence, prefixed by # (optional)
2. The Japanese sentence, prefixed by #jp
3. A natural English translation of the sentence, prefixed by #en (optional)
4. A tokenized version of the Japanese sentence. One token per line, 
with an English translation of the token on the same line separated by a tap character.

These must be one empty line between each sentence.

