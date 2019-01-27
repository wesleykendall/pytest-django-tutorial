from django import shortcuts
from django.views.generic import View


class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return shortcuts.redirect('meme:memes')
        else:
            return shortcuts.redirect('marketing:landing')
