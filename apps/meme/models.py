from django.conf import settings
from django.db import models


class Meme(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url = models.URLField()
    creation_time = models.DateTimeField(auto_now_add=True)
