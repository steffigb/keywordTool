from django.urls import path

from . import views
from accounts import urls
from django.urls import path, include


urlpatterns = [
    path('', views.home, name='index'),
    path('keywords', views.keywords, name='keywords'),
    path('about', views.about, name='about'),
    path('accounts/', include('accounts.urls')),
]
