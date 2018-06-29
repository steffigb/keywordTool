from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('keywords', views.keywords, name='keywords'),
    path('about', views.about, name='about')
]
