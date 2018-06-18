from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

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
    #page = requests.get(input_url)

    #contents = page.content


    #all_as = soup.find_all('a')
    return HttpResponse(output)

    #return HttpResponse("Hier werden die Keywords ausgegeben " + request.GET['url'])
