import six
from google.cloud import translate_v2 as translate


def translate_google(text):
    return _translate_text("en",text)


def _translate_text(target, text):
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    result = translate_client.translate(
        text, target_language=target, source_language="ja", format_="text")

    return result['translatedText']