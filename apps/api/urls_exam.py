from django.conf.urls import url

import apps.api.views_exam_api as views_exam_api

urlpatterns = [
    url(
        r'^(\d+)/change_description$',
        views_exam_api.change_exam_desc,
        name='change_description'
    ),
]
