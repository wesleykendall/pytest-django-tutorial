from django import template
from django.db import models
from django.templatetags.static import static
import django.utils.safestring


register = template.Library()


@register.filter(name='avatar', is_safe=True)
def avatar(model_or_avatar, dim=50):
    avatar_id = model_or_avatar.avatar if issubclass(model_or_avatar.__class__, models.Model) else model_or_avatar
    avatar_slug = avatar_id.lower().replace('_', '-')

    avatar_url = static(f'assets/images/avatars/{avatar_slug}.svg')
    html = f'''
        <div class="rounded-circle border d-inline-block" style="width: {dim}px; height: {dim}px; padding: .35rem">
          <img src="{avatar_url}" class="w-100"/>
        </div>
    '''
    return django.utils.safestring.mark_safe(html)
