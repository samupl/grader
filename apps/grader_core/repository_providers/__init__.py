class AbstractRepositoryProvider:

    def __init__(self, repo_url, local_directory):
        self.repo_url = repo_url
        self.local_directory = local_directory

    def checkout(self) -> str:
        """
        Checkout the repository for the first time. Return the current revision
        number.
        """
        raise NotImplementedError

    def current_revision(self) -> str:
        """
        Get the current revision number.
        """
        raise NotImplementedError

    def update(self):
        """
        Update the repository. Return the current revision number or False, if
        there are no changes on the origin.
        :rtype: str or False
        """
        raise NotImplementedError

    def changed_files(self, current_revision, previous_revision=None):
        """
        Return the list of files changed since the specified revision
        """
        raise NotImplementedError
