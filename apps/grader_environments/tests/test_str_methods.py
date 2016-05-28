from django.test import TestCase

from apps.grader_environments.models import RuntimeEnvironment, RuntimeEnvironmentGroup


class StrMethodsCase(TestCase):
    def test_runtime_env_without_password(self):
        runtime_env = RuntimeEnvironment(
            host='127.0.0.1',
            username='john'
        )
        self.assertEqual(str(runtime_env), 'john@127.0.0.1 (no password set)')

    def test_runtime_env_with_password(self):
        runtime_env = RuntimeEnvironment(
            host='127.0.0.1',
            username='john',
            password='123'
        )
        self.assertEqual(str(runtime_env), 'john@127.0.0.1 (with password)')

    def test_runtime_env_with_port(self):
        runtime_env = RuntimeEnvironment(
            host='127.0.0.1',
            username='john',
            port=22
        )
        self.assertEqual(str(runtime_env), 'john@127.0.0.1:22 (no password set)')

    def test_runtime_env_with_port_and_password(self):
        runtime_env = RuntimeEnvironment(
            host='127.0.0.1',
            username='john',
            port=22,
            password=123
        )
        self.assertEqual(str(runtime_env), 'john@127.0.0.1:22 (with password)')

    def test_runtime_env_group_with_one_environment(self):
        runtime_env_group = RuntimeEnvironmentGroup.objects.create(name='Test group')

        RuntimeEnvironment.objects.create(
            host='127.0.0.1',
            username='john',
            group=runtime_env_group
        )
        self.assertEqual(str(runtime_env_group), 'Test group (1 runtime environment)')

    def test_runtime_env_group_with_more_than_one_environment(self):
        runtime_env_group = RuntimeEnvironmentGroup.objects.create(name='Test group')

        RuntimeEnvironment.objects.create(
            host='127.0.0.1',
            username='john',
            group=runtime_env_group
        )
        RuntimeEnvironment.objects.create(
            host='127.0.0.1',
            username='john',
            group=runtime_env_group
        )
        self.assertEqual(str(runtime_env_group), 'Test group (2 runtime environments)')

    def test_runtime_env_group_without_environments(self):
        runtime_env_group = RuntimeEnvironmentGroup.objects.create(name='Test group')
        self.assertEqual(str(runtime_env_group), 'Test group (no environments)')
