from django.conf.urls import url

import apps.frontend.views_exam as app_exam_views


urlpatterns = [
    url(r'^(\d+)$', app_exam_views.exam_info, name='info'),
    url(r'^(\d+)/scores$', app_exam_views.exam_scores_index, name='scores'),
    url(r'^(\d+)/scores/user$', app_exam_views.exam_scores_single_index,
        name='scores_by_user'),
    url(r'^(\d+)/scores/user/(\w+)$', app_exam_views.exam_scores_single_user,
        name='scores_by_user'),
    url(r'^(\d+)/scores/list', app_exam_views.exam_scores_all_users,
        name='scores_list'),
    url(r'^(\d+)/scores/table', app_exam_views.exam_scores_all_users_table,
        name='scores_table'),
]
