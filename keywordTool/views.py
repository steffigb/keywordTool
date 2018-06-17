from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def keywords(request):
    #request.GET['url']

    keywords = request.GET['url']

    return HttpResponse("Hier werden die Keywords ausgegeben " + request.GET['url'])
