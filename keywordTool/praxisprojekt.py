import requests
from bs4 import BeautifulSoup
import urllib.request

"""
Füge hier weitere imports hinzu, bspw. BeautifulSoup und Rake.

'pass' bedeutet, dass die Funktion gar nichts macht und dient als Platzhalter
für deine Implementierung.
"""

def get_html(url):
    """
    Die Funktion erhält als Parameter eine Url und gibt als Ergebnis (mit
    return) das Html als Text (ein String) zurück.

    Nutze dafür die requests-Bibliothek.

    ACHTUNG: Was passiert, wenn es die Website nicht gibt oder es zu einem
    anderen Fehler kommt?
    """
    page = requests.get(url)
    contents = page.content

    return contents

def get_raw_text(html):
    """
    Die  Funktion erhält als Eingabe mit dem Parameter html einen html-String.
    Dieser wird dann mit Hilfe dieser Funktion 'bereinigt': Sämtliche tags
    sollen entfernt werden, damit am Ende nur noch Text übrig bleibt. Der Text
    wird als String zurückgegeben.

    Nutze dafür die BeautifulSoup-Bibliothek.
    """
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True
    
    soup = BeautifulSoup(html, 'html.parser')

def get_keywords(raw_text):
    """
    Diese Funktion erhält als Eingabe einen Text und gibt als Antwort eine
    Liste von Keywords zurück.

    Dazu verwendet sie die Rake-Bibliothek (da gibt es verschiedene
    Möglichkeiten; ich würde diese: https://github.com/csurfer/rake-nltk
    verwenden.)
    """
    pass

def get_website_keywords(url):
    """
    Diese Funktion erhält als Eingabe eine Url und gibt als Antwort eine Reihe
    von Keywords zurück. Dazu verwendet sie die weiter oben definierten
    Funktionen. Sie kann dann von anderen Funktionen bspw. in Django aufgerufen
    werden.

    Hier ist nichts mehr zu tun :)
    """
    h = get_html(url)
    t = get_raw_text(h)
    k = get_keywords(t)
    return k
