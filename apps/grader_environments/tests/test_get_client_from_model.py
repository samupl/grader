import paramiko
from django.test import SimpleTestCase
from mock import patch, Mock
import parametrized

from apps.grader_environments.models import RuntimeEnvironment
from apps.grader_environments.tools import get_client_from_model


@patch('paramiko.SSHClient', Mock(spec=paramiko.SSHClient))
@parametrized.parametrized_test_case
class GetClientFromModelCase(SimpleTestCase):
    def test_runtime_env_without_password(self):
        runtime_env = RuntimeEnvironment(
            host='127.0.0.1',
            username='john'
        )
        ssh = get_client_from_model(runtime_env)
        ssh.connect.assert_called_with(hostname=runtime_env.host, username=runtime_env.username)

    def test_runtime_env_with_password(self):
        runtime_env = RuntimeEnvironment(
            host='127.0.0.1',
            username='john',
            password='123'
        )
        ssh = get_client_from_model(runtime_env)
        ssh.connect.assert_called_with(hostname=runtime_env.host,
                                       username=runtime_env.username,
                                       password=runtime_env.password)

    def test_runtime_env_with_port(self):
        runtime_env = RuntimeEnvironment(
            host='127.0.0.1',
            username='john',
            port=22
        )
        ssh = get_client_from_model(runtime_env)
        ssh.connect.assert_called_with(hostname=runtime_env.host,
                                       username=runtime_env.username,
                                       port=runtime_env.port)

    def test_runtime_env_with_password_and_port(self):
        runtime_env = RuntimeEnvironment(
            host='127.0.0.1',
            username='john',
            password='123',
            port=23
        )
        ssh = get_client_from_model(runtime_env)
        ssh.connect.assert_called_with(hostname=runtime_env.host,
                                       username=runtime_env.username,
                                       password=runtime_env.password,
                                       port=runtime_env.port)

    @parametrized.parametrized(args=[[1], [1.0], [object], [float], [int], [''], [b''], [str], [True], [False], [None]])
    def invalid_type(self, obj):
        self.assertRaises(TypeError, lambda: get_client_from_model(obj))
