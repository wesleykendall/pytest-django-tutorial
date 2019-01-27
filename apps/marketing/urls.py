from django.urls import path
from stronghold.decorators import public

import apps.marketing.views as marketing_views


app_name = 'marketing'
urlpatterns = [
    path('', public(marketing_views.Landing.as_view()), name='landing')
]
