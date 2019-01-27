import django.contrib.auth.views as auth_views
from django.urls import path
from stronghold.decorators import public

import apps.user.views as user_views


app_name = 'user'
urlpatterns = [
    path('login/', public(user_views.Login.as_view()), name='login'),
    path('logout/', auth_views.logout_then_login, name='logout'),
    path('register/', public(user_views.Register.as_view()), name='register'),
]
