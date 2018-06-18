from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from rake_nltk import Rake

def home(request):
    return render(request, 'home.html')

# Verarbeitet den inhalt der ausgegebenen URL weiter

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def keywords(request):

    input_url = request.GET['url']

    html = urllib.request.urlopen(input_url).read()
    soup = BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text = True)
    visible_texts = filter(tag_visible, texts)

    output = u" ".join(t.strip() for t in visible_texts)

    # Uses stopwords for english from NLTK, and all puntuation characters by
    # default
    r = Rake(min_length = 1, max_length = 2, language="german")

    # Extraction given the text.
    r.extract_keywords_from_text(output)

    # To get keyword phrases ranked highest to lowest.
    # phrases = r.get_ranked_phrases()

    # To get keyword phrases ranked highest to lowest with scores.
    phrases = r.get_ranked_phrases_with_scores()

    #page = requests.get(input_url)

    #contents = page.content

    def pretty(score, kw):
        return "<p>" + kw + " (" + str(score) + ")</p>"

    nice_phrases = "\n".join([pretty(score, kw) for (score, kw) in r.get_ranked_phrases_with_scores()])

    #all_as = soup.find_all('a')
    return HttpResponse(nice_phrases)

    #return HttpResponse("Hier werden die Keywords ausgegeben " + request.GET['url'])
