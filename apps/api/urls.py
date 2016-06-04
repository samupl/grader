from django.conf.urls import url, include
from .urls_exam import urlpatterns as urlpatterns_exam
from .urls_scenario import urlpatterns as urlpatterns_scenario


urlpatterns = [
    url(r'^exam/', include(urlpatterns_exam, namespace='exam')),
    url(r'^scenario/', include(urlpatterns_scenario, namespace='scenario'))
]
