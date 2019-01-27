from django.views.generic import TemplateView


class Memes(TemplateView):
    template_name = 'meme/memes.html'
