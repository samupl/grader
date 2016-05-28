from django.contrib import admin


# region ModelAdmin class definitions
from apps.grader_environments.models import RuntimeEnvironment, RuntimeEnvironmentGroup


class RuntimeEnvironmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'host', 'username', 'port', 'group']
    search_fields = ['name', 'host', 'username', 'port', 'group']
    list_filter = ['host', 'username', 'port', 'group']


class RuntimeEnvironmentGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'environment_count']
    search_fields = ['name']

    @staticmethod
    def environment_count(obj):
        return obj.runtimeenvironment_set.count()

# endregion


# region Model registration to admin site framework
admin.site.register(RuntimeEnvironment, RuntimeEnvironmentAdmin)
admin.site.register(RuntimeEnvironmentGroup, RuntimeEnvironmentGroupAdmin)
# endregion
