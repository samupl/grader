from django.contrib import admin
from django.db.models import F, Sum
from django.utils.translation import ugettext_lazy as _

from apps.grader_core.models import Exam, Task, Scenario, Repository


# region Tools
def configure_admin_site(url_admin):
    site_title = _('Grader administration')
    url_admin.site.site_header = site_title
    url_admin.site.index_title = site_title
    url_admin.site.site_title = site_title
# endregion


# region ModelAdmin class definitions
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_start', 'date_end', 'repository']
    search_fields = ['name', 'repository']

    def get_in_progress(self, obj):
        pass

    get_in_progress.admin_order_field = 'name'


class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'path', 'exam', 'points']
    search_fields = ['title', 'path']
    list_filter = ['exam__name']

    def points(self, obj):
        task_points = obj.scenario_set.all().aggregate(points=Sum(F('points')))
        task_points = task_points.get('points')
        return task_points if task_points else 0


class ScenarioAdmin(admin.ModelAdmin):
    list_display = ['task', 'scenario_type', 'points']


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ['repository_id', 'repository_type', 'url']
    search_fields = ['repository_id', 'repository_type', 'url']
    list_filter = ['repository_type']

# endregion


# region Model registration to admin site framework
admin.site.register(Exam, ExamAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(Repository, RepositoryAdmin)
# endregion
