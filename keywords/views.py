from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from . import phrases

def home(request):
    context = {}
    template = loader.get_template('keywords/home.html')
    return HttpResponse(template.render(context, request))

def keywords(request):
    input_url = request.GET['url']
    ranked_phrases = phrases.get_website_keywords(input_url)

    def pretty(score, kw):
        return "<p>" + kw + " (" + str(score) + ")</p>"

    nice_phrases = "\n".join([pretty(score, kw) for (score, kw) in ranked_phrases])
    return HttpResponse(nice_phrases)
