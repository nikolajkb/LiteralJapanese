import pykakasi


def translate(jp):
    kakasi = pykakasi.kakasi()
    kakasi.setMode("K", "a")
    kakasi.setMode("r", "Hepburn")
    converter = kakasi.getConverter()
    hepburn = converter.do(jp)
    return hepburn
