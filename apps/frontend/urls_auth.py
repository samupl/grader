from django.conf.urls import url

import django.contrib.auth.views

urlpatterns = [
    url(r'^sign-out$', django.contrib.auth.views.logout, name='sign-out',
        kwargs={'template_name': 'frontend/auth/sign_out.html'}),
    url(r'^sign-in$', django.contrib.auth.views.login, name='sign-in',
        kwargs={'template_name': 'frontend/auth/sign_in.html'}),
]
