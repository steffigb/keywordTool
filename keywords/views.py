from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from . import phrases
from .models import KeywordsList, Keyword

def home(request):
    context = {}
    template = loader.get_template('keywords/home.html')
    return HttpResponse(template.render(context, request))

def keywords_create(request):
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

    # create a new KeywordsList
    kw_list = KeywordsList(description="", url=input_url, author=request.user)
    kw_list.save()

    # add all Keywords to the fresh KeywordsList
    for keyword in top_keywords:
        kw_obj = Keyword(kw_list=kw_list, phrase=keyword[1], score=keyword[0])
        kw_obj.save()

    return HttpResponseRedirect(reverse('list', args=(kw_list.id,)))

def keyword_list(request, list_id):
    kw_list = get_object_or_404(KeywordsList, pk=list_id)
    keywords = Keyword.objects.filter(kw_list=kw_list)

    context = {
        "phrases": keywords,
        "list": kw_list
    }
    template = loader.get_template('keywords/keywords-output.html')
    return HttpResponse(template.render(context, request))

def about(request):
    context = {}
    template = loader.get_template('keywords/about.html')
    return HttpResponse(template.render(context, request))

def csv_export(request, list_id):
    kw_list = get_object_or_404(KeywordsList, pk=list_id)
    keywords = Keyword.objects.filter(kw_list=kw_list)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="keywords.csv"'

    t = loader.get_template('keywords/csv_export.txt')
    c = {
        'data': keywords,
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
