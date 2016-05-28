import paramiko

from apps.grader_environments.models import RuntimeEnvironment


def get_client_from_model(runtime_env):
    if not isinstance(runtime_env, RuntimeEnvironment):
        raise TypeError('You must pass a RuntimeEnvironment instance')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    connect_params = {
        'hostname': runtime_env.host,
        'username': runtime_env.username
    }

    if runtime_env.password:
        connect_params['password'] = runtime_env.password

    if runtime_env.port:
        connect_params['port'] = runtime_env.port

    ssh.connect(**connect_params)
    return ssh
