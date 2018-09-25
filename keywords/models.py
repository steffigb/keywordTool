from django.conf import settings
from django.db import models

class KeywordsList(models.Model):
    description = models.TextField(max_length=200)
    url = models.CharField(max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

class Keyword(models.Model):
    kw_list = models.ForeignKey(KeywordsList, on_delete=models.CASCADE)
    phrase = models.CharField(max_length=300)
    score = models.FloatField(default=0)
    cpc = models.FloatField(default=None, null=True)
    cpm = models.FloatField(default=None, null=True)
    competition = models.FloatField(default=None, null=True)
