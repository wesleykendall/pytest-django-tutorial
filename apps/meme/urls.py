from django.urls import path

import apps.meme.views as meme_views


app_name = 'meme'
urlpatterns = [
    path('memes/', meme_views.Memes.as_view(), name='memes'),
]
