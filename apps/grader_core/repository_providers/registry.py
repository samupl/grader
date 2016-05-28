from apps.grader_core.repository_providers.svn_provider import \
    SubversionProvider


class FactoryRegistry:
    _registry = {}

    @classmethod
    def register(cls, repo_name, repo_cls):
        cls._registry[repo_name] = repo_cls

    @classmethod
    def get(cls, repo_name):
        return cls._registry[repo_name]


registry = FactoryRegistry()

registry.register('svn', SubversionProvider)
