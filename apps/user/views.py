from django import urls
from django.contrib import auth
import django.contrib.auth.forms as auth_forms
import django.contrib.auth.views as auth_views
from django.views.generic.edit import CreateView

import apps.user.forms as user_forms


class Login(auth_views.LoginView):
    template_name = 'user/login.html'
    form_class = user_forms.Login


class Register(CreateView):
    template_name = 'user/register.html'
    form_class = auth_forms.UserCreationForm
    success_url = urls.reverse_lazy('home')

    def form_valid(self, *args, **kwargs):
        resp = super().form_valid(*args, **kwargs)

        user = self.object
        auth.login(self.request, user)

        return resp
