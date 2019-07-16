from django.shortcuts import render
import requests
from newsapi import NewsApiClient
from decouple import config
from .models import *


def home(request):
    NEWS_API_KEY = config('NEWS_API_KEY', default='')
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    content = {}
    country = ""
    category = ""
    article = ""
    top_headlines = {"status": "400"}
    if 'country' in request.GET:
        country = request.GET['country']
        country = country.lower()
    if 'category' in request.GET:
        category = request.GET['category']
        category = category.lower()
    if category and country:
        top_headlines = newsapi.get_top_headlines(
            category=category, country=country, language='en')
        if request.user.is_authenticated:
            print(request.user)
            if 'article' in request.GET:
                article = request.GET['article']
                # article = article.lower()
                print(article)
                print(top_headlines['articles'][int(article)])
                news = top_headlines['articles'][int(article)]
                newsExist = liked.objects.filter(url=news['url']).exists()
                if newsExist == False:
                    user = request.user
                    category = category
                    country = country
                    author = news['author']
                    image = news['urlToImage']
                    date = news['publishedAt']
                    source = news['source']['name']
                    url = news['url']
                    title = news['title']
                    description = news['description']
                    liked.objects.create_obj(
                        user, category, country, author, image, date, source, url, title, description)

    elif country:
        top_headlines = newsapi.get_top_headlines(
            country=country, language='en')

    status = top_headlines['status']
    if status == 'ok':
        totalResults = top_headlines['totalResults']
        articles = top_headlines['articles']
        content = {'status': status,
                   'totalResults': totalResults, 'articles': articles, 'country': country, 'category': category}
    return render(request, 'news.html', content)


def favourite(request):
    if request.user.is_authenticated:
        favs = liked.objects.all()
        return render(request, 'favs.html', {'articles': favs})
    else:
        return render(request, "<h1>NOT FOUND</h1>")
