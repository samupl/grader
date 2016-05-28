from django.conf.urls import url, include

import apps.frontend.views as app_views

import apps.frontend.urls_exam


urlpatterns = [
    url(r'^$', app_views.home, name='home'),
    url(r'^exam/', include(apps.frontend.urls_exam, namespace='exam')),
    url(r'^statistics.json$', app_views.statistics, name='statistics'),
    url(r'^backend_assets/constants_and_translations\.js$', app_views.javascript, name='javascript')
]
