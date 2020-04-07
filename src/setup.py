from setuptools import setup

setup(
    name='LiteralJapaneseTranslation',
    version='0.1',
    packages=[''],
    package_dir={'': 'src'},
    url='https://github.itu.dk/nbje/LiteralJapaneseTranslation',
    license='GNU GPLv3',
    author='Nikolaj Bjerregaard',
    author_email='nbje@itu.dk',
    description='Grammar preserving Japanese to English translation',
    install_requires=[
        "sudachipy",
        "pickledb",
        "six",
        "google-cloud-translate==2.0.0",
        "nltk",
        "pykakasi",
        "japanese-numbers-python",
        "millify",
        "colored",
        "gensim"
    ]
)
