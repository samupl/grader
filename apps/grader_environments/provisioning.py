import logging

import jsonpickle
import os
from django.conf import settings

logger = logging.getLogger('grader')


class GraderProvisioningManager:
    def __init__(self, re_group):
        self.re_group = re_group
        self.sftp = None

    def provision(self):
        logger.debug('Running provisioning for group: %s', self.re_group)
        for runtime_env in self.re_group.runtimeenvironment_set.all():
            logger.debug('Provisioning: %s', runtime_env)
            self.provision_env(runtime_env)

    def provision_env(self, runtime_env):
        self.upload_base_files_to_env(runtime_env)

    def put_directory(self, local_path, remote_path):
        parent, target = os.path.split(local_path)
        os.chdir(parent)

        for walker in os.walk(target):
            try:
                self.sftp.mkdir(os.path.join(remote_path, walker[0]))
            except IOError:
                pass

            for file in walker[2]:
                if file.endswith('.pyc'):  # Skip compiled pyc files
                    continue

                self.sftp.put(os.path.join(walker[0], file),
                              os.path.join(remote_path, walker[0], file))

    def upload_base_files_to_env(self, runtime_env):
        self.sftp = runtime_env.paramiko_sftp_client
        # Put SSHRPC server

        self.put_directory(os.path.join(settings.BASE_DIR, 'lib', 'sshrpc'), '.')
        # Put jsonpickle dependency
        self.put_directory(os.path.dirname(jsonpickle.__file__), '.')
        # Put grader sshrpc endpoint server
        self.sftp.put(os.path.join(settings.BASE_DIR, 'lib', 'sshrpc_endpoint.py'), 'sshrpc_endpoint.py')
        runtime_env.close_ssh()


class TaskProvisioningManager:
    def __init__(self, runtime_env, files):
        self.runtime_env = runtime_env
        self.files = files
        self.sftp = None

    def provision(self):
        self.sftp = self.runtime_env.paramiko_sftp_client
        for file in self.files:
            basename = os.path.basename(file)
            self.sftp.put(file, basename)
            self.sftp.chmod(basename, 0o755)
