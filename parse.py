import string
from bs4 import BeautifulSoup


def get_body_words(raw_html):
    bs = BeautifulSoup(raw_html, "html.parser")

    for script in bs(["script", "style"]):
        script.extract() #discard

    return ' '.join(''.join(bs.body.get_text()).split())


def get_words(raw_html):
    # remove ascii punctuation
    remove_punctuation_map = dict((ord(char), unicode(" ")) for char in string.punctuation)
    all_words = ' '.join(word.translate(remove_punctuation_map).strip() for word in get_body_words(raw_html).split())

    # remove whitespace
    words = ' '.join(all_words.split())

    # remove single chrs
    words = (word for word in words.split() if len(word) > 1)

    return words

