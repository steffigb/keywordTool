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

    context = {
        "phrases": phrases.get_website_keywords(input_url)
    }
    template = loader.get_template('keywords/keywords-output.html')
    return HttpResponse(template.render(context, request))
