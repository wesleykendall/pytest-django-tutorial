from django.urls import path

import apps.meme.views as meme_views


app_name = 'meme'
urlpatterns = [
    path('memes/', meme_views.Memes.as_view(), name='memes'),
    path('choose/', meme_views.Choose.as_view(), name='choose'),
    path('create/<int:id>/<path:url>/', meme_views.Create.as_view(), name='create'),
]
