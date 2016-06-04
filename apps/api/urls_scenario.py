from django.conf.urls import url

import apps.api.views_scenario_api as views_exam_api

urlpatterns = [
    url(
        r'^getFromExecutable',
        views_exam_api.get_scenario_info_from_executable,
        name='get_from_executable'
    ),
]
