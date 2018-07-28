from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required

from . import phrases
from .models import KeywordsList, Keyword

def home(request):
    context = {}
    template = loader.get_template('keywords/home.html')
    return HttpResponse(template.render(context, request))

def keywords(request):
    request_params = request.POST
    input_url = request_params['url']
    language = request_params['language']
    numberOfKeywords = request_params['top']
    phraseMinLength = request_params['phraseMinLength']
    phraseMaxLength = request_params['phraseMaxLength']

    all_phrases = phrases.get_website_keywords(input_url, language,
                        phraseMinLength, phraseMaxLength)

    top_keywords = []
    if numberOfKeywords == 'all':
        top_keywords = all_phrases
    else:
        topNumber = int(numberOfKeywords)
        top_keywords = all_phrases[:topNumber]

    context = {
        "phrases": top_keywords
    }
    template = loader.get_template('keywords/keywords-output.html')
    return HttpResponse(template.render(context, request))

def about(request):
    context = {}
    template = loader.get_template('keywords/about.html')
    return HttpResponse(template.render(context, request))

def csv_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="keywords.csv"'

    csv_data = (
        (3.0, "shih tzu"),
        (2.0, "hunde welpe"),
        (1.0, "lustige hundchen"),
    )

    t = loader.get_template('keywords/csv_export.txt')
    c = {
        'data': csv_data,
    }

    response.write(t.render(c))
    return response

@login_required
def keyword_list_overview(request):
    my_keyword_lists = KeywordsList.objects.filter(author=request.user)

    context = {
        "lists": my_keyword_lists
    }
    template = loader.get_template('keywords/overview.html')
    return HttpResponse(template.render(context, request))
