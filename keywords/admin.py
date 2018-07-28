from django.contrib import admin

# Register your models here.
from .models import KeywordsList, Keyword

admin.site.register(KeywordsList)
admin.site.register(Keyword)
