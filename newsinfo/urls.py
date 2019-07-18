from django.urls import path
from .views import *
from django.conf.urls import url

urlpatterns = [
    path('', home, name='home'),
    path('favourite/', favourite, name='fav'),
    path('signup/', signup, name='signup'),
    path('delete/<int:id>', delete, name='delete'),
    url(r'^account_activation_sent/$', account_activation_sent,
        name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
]
