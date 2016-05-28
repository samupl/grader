from django.contrib import admin
from .models import Result, LatestResult


# region ModelAdmin class definitions
class ResultAdmin(admin.ModelAdmin):
    list_display = ['check_date', 'user', 'scenario', 'points', 'get_completed']

    def has_add_permission(self, request, obj=None):
        return False

    def get_completed(self, obj):
        return obj.points == obj.scenario.points

    get_completed.boolean = True
    get_completed.short_description = 'Task completed'
# endregion


# region Model registration to admin site framework
admin.site.register(Result, ResultAdmin)
admin.site.register(LatestResult, ResultAdmin)
# endregion
