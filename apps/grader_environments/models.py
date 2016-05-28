import paramiko
from django.db import models
from django.utils.translation import ugettext_lazy as _

from lib.sshrpc.client import SSHRPCClient


class RuntimeEnvironmentGroup(models.Model):
    name = models.CharField(_('Name'), max_length=128)

    def humanize_environment_count(self):
        count = self.runtimeenvironment_set.count()
        if count == 0:
            return _('no environments')
        elif count == 1:
            return _('1 runtime environment')
        else:
            return '{count} {count_str}'.format(
                count=count,
                count_str=_('runtime environments')
            )

    def __str__(self):
        return '{name} ({env_count_str})'.format(
            name=self.name,
            env_count_str=self.humanize_environment_count()
        )


class RuntimeEnvironment(models.Model):
    name = models.CharField(_('Name'), max_length=128)
    host = models.CharField(_('Host'), max_length=512)
    username = models.CharField(_('Username'), max_length=256)
    password = models.CharField(_('Password'), max_length=512, null=True, blank=True)
    port = models.PositiveIntegerField(_('Port'), null=True, blank=True)
    group = models.ForeignKey(RuntimeEnvironmentGroup)

    def __str__(self):
        return '{user}@{host}{port} ({password_info})'.format(
            user=self.username,
            host=self.host,
            port=':{}'.format(self.port) if self.port else '',
            password_info=_('with password') if self.password else _('no password set')
        )

    def close_ssh(self):
        if hasattr(self, '_ssh_client'):
            self._ssh_client.close()

    @property
    def ssh_rpc_client(self):
        ssh = self.paramiko_ssh_client
        client = SSHRPCClient(ssh)
        return client

    @property
    def paramiko_ssh_client(self):
        # if hasattr(self, '_ssh_client'):
        #     return self._ssh_client

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        connect_kwargs = {
            'username': self.username,
            'hostname': self.host,
            'port': self.port if self.port is not None else 22
        }

        if self.password:
            connect_kwargs['password'] = self.password

        ssh_client.connect(**connect_kwargs)
        self._ssh_client = ssh_client
        return self._ssh_client

    @property
    def paramiko_sftp_client(self):
        sftp = self.paramiko_ssh_client
        sftp = sftp.open_sftp()
        return sftp

    def __del__(self):
        self.close_ssh()
