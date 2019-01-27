from django.conf import settings
from django.contrib import admin
from django.views.generic import RedirectView
from django.urls import include, path
from stronghold.decorators import public

import meme_creator.views


urlpatterns = [
    path('', public(meme_creator.views.Home.as_view()), name='home'),
    path('admin/', admin.site.urls),
    path('favicon.ico', public(RedirectView.as_view(url='static/assets/images/favicons/favicon-32x32.png'))),
    path('marketing/', include('apps.marketing.urls')),
    path('meme/', include('apps.meme.urls')),
    path('user/', include('apps.user.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
