# Literal Japanese Translation
**Note: this system was created as a Bachelor's project and should not be viewed as a production-ready library**
#### About
Literal Japanese is a Japanese-English translator that translates word by word and thus preserves Japanese grammar. 
Literal Japanese is intended as a tool for Japanese learners who want to learn about Japanese sentence structure.
Examples of the type of translations this program produces can be seem in the sentences_dev and sentences_test documents in the data folder. 
More in depth information can be read in the report written about the project: https://github.com/nikolajkb/LiteralJapaneseMirror/blob/master/data/Literal%20Japanese%20report.pdf
#### Installation
The system is developed for Python 3.6.8 and may not work for other versions.
1. run ``pip install .`` to install dependencies
2. install sudachipy dictionary using\
`pip install https://object-storage.tyo2.conoha.io/v1/nc_2520839e1f9641b08211a5c85243124a/sudachi/SudachiDict_core-20191224.tar.gz`
3. Run the NltkDownload.py in script folder to download nltk packages
4. Make sure that Visual C++ is installed (should only be necessary for Windows)\
   https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads
##### Usage
1. run LiteralJapanese.py\
use the `-h` argument to display available commands
2. example command: ``LiteralJapanese.py --test "..\data\sentences_dev.txt" -v``
3. must be run as administrator on Windows

The first run will take more time, as the program will generate necessary files. 

#### Translating
Translations can be done interactively in the command line:\
`LiteralJapanese.py --interactive`\
A translation can also be saved to a specified file:\
`--translate "勉強すればするほど分かる。" --output "translation.txt"`\
This will write the translated tokens one line at a time, first the Japanese then the English separated by a tap (`\t`) character.\
A file containing one or more sentences can also be specified:\
`--batch-translate --input "input.txt" --output "output.txt"`

(will append to output file if it already exists)

##### Using python
Translations can be done programmatically by calling the `translate(text)` function located in LiteralJapanese.py.
This will return a list of Translation objects that have three attributes.
1. ``japanese`` (the Japanese token)
2. ``english`` (the English translation of the token)
3. ``token`` (a token object with info on POS etc., refer to Tokenizer.py)

#### Testing
To test the system, you need to provide a test file. Two test files are provided in the data folder.\
Example command:\
`LiteralJapanese.py --test "..\data\sentences_dev.txt" -v` \
You can also test only the tokenization using the --tt command.\
Using the ``-v`` argument prints the gold and system translations.\
\
The system can count translations as correct if they are synonyms of the gold translation using the ``-p`` argument. 
This requires two additional files.
1. Google news vectors  
https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?usp=sharing 
(from https://code.google.com/archive/p/word2vec/)  
must be located in ``data/GoogleNewsVectors/GoogleNews-vectors-negative300.bin``
2. Paraphrase database \
http://paraphrase.org/#/download (small version) \
must be located in `data/PPDB/ppdb-2.0-s-all`

##### Test file format
A test file consists of Sentences. Each sentence has four elements.
1. A numeric id for the sentence, prefixed by # 
2. The Japanese sentence, prefixed by #jp
3. A natural English translation of the sentence, prefixed by #en 
4. A tokenized version of the Japanese sentence. One token per line, 
with an English translation of the token on the same line separated by a tap character.

There is one empty line between each sentence.

