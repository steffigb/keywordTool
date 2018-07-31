from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import transaction
import requests

from . import phrases
from .models import KeywordsList, Keyword

def home(request, error="", url=""):
    context = {"error": error, "url": url}
    template = loader.get_template('keywords/home.html')
    return HttpResponse(template.render(context, request))

@transaction.atomic
def save_keywords(kw_list, top_keywords):
    """
    Database updates were very slow. After some googling I found this solution.
    https://docs.djangoproject.com/en/dev/topics/db/transactions/#django.db.transaction.atomic
    """
    for keyword in top_keywords:
        kw_obj = Keyword(kw_list=kw_list, phrase=keyword["phrase"], score=keyword["score"])
        kw_obj.save()

def keywords_create(request):
    # make sure to handle only POST requests in this view
    if not request.POST:
        return HttpResponseRedirect(reverse('index'))

    # read in parameters
    request_params = request.POST
    input_url = request_params['url']
    language = request_params['language']
    numberOfKeywords = request_params['top']
    phraseMinLength = request_params['phraseMinLength']
    phraseMaxLength = request_params['phraseMaxLength']

    # make sure URL exists
    try:
        request = requests.get(input_url)
    except:
        context = {"error": "Website does not exist", "url": input_url}
        template = loader.get_template('keywords/home.html')
        return HttpResponse(template.render(context, request))

    # get keywords
    all_phrases = phrases.get_website_keywords(input_url, language,
                        phraseMinLength, phraseMaxLength)

    # take only chosen number of keywords
    top_keywords = []
    if numberOfKeywords == 'all':
        top_keywords = all_phrases
    else:
        topNumber = int(numberOfKeywords)
        top_keywords = all_phrases[:topNumber]

    # if user is authenticated, store keywords and redirect to keyword_list view
    if request.user.is_authenticated:
        # create a new KeywordsList
        kw_list = KeywordsList(description="", url=input_url, author=request.user)
        kw_list.save()

        # add all Keywords to the fresh KeywordsList
        save_keywords(kw_list, top_keywords)

        return HttpResponseRedirect(reverse('list', args=(kw_list.id,)))

    # if user is not authenticated, render keywords directly
    else:
        context = {
            "phrases": top_keywords,
            "list": {
                "url": input_url,
                "description": ""
            },
            "login": False
        }
        template = loader.get_template('keywords/keywords-output.html')
        return HttpResponse(template.render(context, request))

def keyword_list(request, list_id):
    kw_list = get_object_or_404(KeywordsList, pk=list_id)
    keywords = Keyword.objects.filter(kw_list=kw_list)

    if request.POST:
        all_keys = request.POST.keys()
        keep_keywords = [int(k.replace("keep-", "")) for k in all_keys if "keep-" in k]

        # update list and keywords
        for k in all_keys:
            if "description-" in k:
                kw_list.description = request.POST[k]
                kw_list.save()

            if "keyword-" in k:
                keyword_id = int(k.replace("keyword-", ""))
                change_text = request.POST[k]
                update_kw = Keyword.objects.get(pk=keyword_id)
                if update_kw.phrase != change_text:
                    update_kw.phrase = change_text
                    update_kw.save()

        # delete keywords
        for keyword_object in keywords:
            if not keyword_object.id in keep_keywords:
                keyword_object.delete()

        return HttpResponseRedirect(reverse('list', args=(list_id,)))

    else:
        context = {
            "phrases": keywords,
            "list": kw_list,
            "login": True
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
