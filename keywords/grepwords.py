import requests
from django.conf import settings

def lookup(query):
    try:
        url = 'http://api.grepwords.com/lookup?apikey=' + settings.GREPWORDS_API_KEY + '&q=' + query
        response = requests.get(url)
        return response.json()
    except:
        print("Error at lookup-query.")
        return []

def related(query):
    try:
        url = 'http://api.grepwords.com/related?apikey=' + settings.GREPWORDS_API_KEY + '&q=' + query
        response = requests.get(url)
        return response.json()
    except:
        print("Error at related-query.")
        return []

def query_helper(keywords):
    return "|".join(keywords)
