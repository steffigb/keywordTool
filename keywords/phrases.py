import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
from rake_nltk import Rake

def get_html(url):
    """
    Die Funktion erhält als Parameter eine Url und gibt als Ergebnis (mit
    return) das Html als Text (ein String) zurück.

    ACHTUNG: Was passiert, wenn es die Website nicht gibt oder es zu einem
    anderen Fehler kommt?
    """
    page = requests.get(url)
    contents = page.content

    return contents

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def get_raw_text(html):
    """
    Die  Funktion erhält als Eingabe mit dem Parameter html einen html-String.
    Dieser wird dann mit Hilfe dieser Funktion 'bereinigt': Sämtliche tags
    sollen entfernt werden, damit am Ende nur noch Text übrig bleibt. Der Text
    wird als String zurückgegeben.
    """
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text = True)
    visible_texts = filter(tag_visible, texts)

    return u" ".join(t.strip() for t in visible_texts)

def get_keywords(raw_text, language, phraseMinLength, phraseMaxLength):
    """
    Diese Funktion erhält als Eingabe einen Text und gibt als Antwort eine
    Liste von Keywords zurück.

    Dazu verwendet sie die Rake-Bibliothek.
    """
    # Uses stopwords for english from NLTK, and all puntuation characters by
    # default
    r = Rake(min_length = int(phraseMinLength),
             max_length = int(phraseMaxLength),
             language=language)

    # Extraction given the text.
    r.extract_keywords_from_text(raw_text)

    # To get keyword phrases ranked highest to lowest.
    # phrases = r.get_ranked_phrases()

    # To get keyword phrases ranked highest to lowest with scores.
    return r.get_ranked_phrases_with_scores()

def get_filtered_keywords(keywords):
    """
    TODO: Keywords filtern. Nicht vergessen: Die List der keywords ist so auf-
          gebaut [(12.0, "keyword1"), (10.2 "keyword2"), ...]
    """
    return keywords

def get_website_keywords(url, language, phraseMinLength, phraseMaxLength):
    """
    Diese Funktion erhält als Eingabe eine Url und gibt als Antwort eine Reihe
    von Keywords zurück. Dazu verwendet sie die weiter oben definierten
    Funktionen. Sie kann dann von anderen Funktionen bspw. in Django aufgerufen
    werden.
    """
    h = get_html(url)
    t = get_raw_text(h)
    k = get_keywords(t, language, phraseMinLength, phraseMaxLength)
    f = get_filtered_keywords(k)
    return k
