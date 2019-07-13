from django.shortcuts import render
import requests
from newsapi import NewsApiClient
from decouple import config


def home(request):
    NEWS_API_KEY = config('NEWS_API_KEY', default='')
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    content = {}
    country = ""
    category = ""

    if 'country' in request.GET:
        country = request.GET['country']
        country = country.lower()
    if 'category' in request.GET:
        category = request.GET['category']
        category = category.lower()
    if category and country:
        top_headlines = newsapi.get_top_headlines(
            category=category, country=country, language='en')
    elif country:
        top_headlines = newsapi.get_top_headlines(
            country=country, language='en')

        status = top_headlines['status']
        if status == 'ok':
            totalResults = top_headlines['totalResults']
            articles = top_headlines['articles']
            content = {'status': status,
                       'totalResults': totalResults, 'articles': articles}
    return render(request, 'news.html', content)
