from django.shortcuts import render
import requests
from newsapi import NewsApiClient
from decouple import config
from .models import *


from django.http import HttpResponseRedirect
from django.conf import settings
from django.views.generic import DetailView, ListView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import TemplateView
from django.db.models import Q
from .forms import *
from .tokens import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


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
    # else:
        # return render(request, "<h1>NOT FOUND</h1>")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')
