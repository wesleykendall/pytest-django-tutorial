import logging

from django import urls
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from apps.meme import img_flip_api
import apps.meme.forms as meme_forms
import apps.meme.models as meme_models


LOGGER = logging.getLogger(__name__)


class Memes(TemplateView):
    template_name = 'meme/memes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['memes'] = (
            meme_models.Meme.objects.filter(user=self.request.user).order_by('-creation_time')
        )
        return context


class Choose(TemplateView):
    template_name = 'meme/choose.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['memes'] = img_flip_api.get_memes()
        except img_flip_api.ImgFlipError as exc:
            context['error'] = str(exc)
        return context


class Create(FormView):
    template_name = 'meme/create.html'
    form_class = meme_forms.Create
    success_url = urls.reverse_lazy('meme:memes')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['template_id'] = self.kwargs['id']
        return kwargs

    def form_valid(self, form):
        meme_models.Meme.objects.create(user=self.request.user, url=form.cleaned_data['url'])
        return super().form_valid(form)
