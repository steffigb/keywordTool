from django.urls import path

from . import views
from accounts import urls
from django.urls import path, include


urlpatterns = [
    path('', views.home, name='index'),
    path('keywords', views.keywords_create, name='keywords'),
    path('<int:list_id>/list/', views.keyword_list, name='list'),
    path('about', views.about, name='about'),
    path('<int:list_id>/csv_export/', views.csv_export, name='csv_export'),
    path('accounts/', include('accounts.urls')),
    path('overview', views.keyword_list_overview, name='overview'),
]
