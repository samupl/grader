import svn.remote
import svn.local

from apps.grader_core.repository_providers import AbstractRepositoryProvider


class SubversionProvider(AbstractRepositoryProvider):
    """
    A provider class for subversion-based repositories.
    """

    def current_revision(self):
        local_client = svn.local.LocalClient(self.local_directory)
        return local_client.info().get('commit_revision')

    def update(self):
        local_client = svn.local.LocalClient(self.local_directory)
        previous_revision = self.current_revision()
        local_client.run_command('update', args=[self.local_directory])
        current_revision = self.current_revision()
        if current_revision != previous_revision:
            return current_revision
        return False

    def changed_files(self, current_revision, previous_revision=None):
        local_client = svn.local.LocalClient(self.local_directory)
        changed_files = local_client.run_command('diff', args=[
            self.local_directory,
            '-r',
            '{}:{}'.format(
                previous_revision if previous_revision else 0,
                current_revision),
            '--summarize'
        ])
        return [f.split()[1] for f in changed_files]

    def checkout(self):
        remote_client = svn.remote.RemoteClient(self.repo_url)
        remote_client.checkout(self.local_directory)
        return self.current_revision()
