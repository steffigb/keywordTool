from django.urls import path

from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_view, name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
]
