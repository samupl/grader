import datetime

from django.db import models
from django.db.models import Sum
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class Repository(models.Model):
    TYPE_SVN = 'svn'
    TYPE_GIT = 'git'
    TYPE_MERCURIAL = 'hg'

    REPOSITORY_TYPE_CHOICES = {
        TYPE_SVN: 'Subversion (SVN)',
        TYPE_GIT: 'GIT',
        TYPE_MERCURIAL: 'Mercurial (hg)',
    }

    repository_id = models.CharField(_('Repository id'), max_length=128, unique=True)
    repository_type = models.CharField(_('Type'), max_length=24, choices=list(REPOSITORY_TYPE_CHOICES.items()))
    url = models.CharField(_('URL'), max_length=1024)

    def __str__(self):
        return '{id} ({repo_type}, {url})'.format(
            id=self.repository_id,
            repo_type=self.repository_type,
            url=self.url
        )

    class Meta:
        verbose_name = _('Repository')
        verbose_name_plural = _('Repositories')


class Exam(models.Model):
    name = models.CharField(_('Exam short name'), max_length=128, unique=True)
    description = models.TextField(_('Description'), max_length=2048)
    date_start = models.DateTimeField(_('Starting date & time'))
    date_end = models.DateTimeField(_('End date & time'))
    repository = models.ForeignKey(Repository)

    @property
    def in_progress(self):
        """
        Indicates whether the exam is currently in progress or not. An exam will be in progress if the current time is
        between the exams start and end date.

        :return: True if the exam is in progress or False
        :rtype: bool
        """
        now = datetime.datetime.now()
        return self.date_start < now < self.date_end

    def time_left(self):
        now = timezone.now()
        now = now - datetime.timedelta(microseconds=now.microsecond)
        delta = self.date_end - now
        return delta

    def __str__(self):
        return u'{name} ({progress_status}, {date_start} - {date_end})'.format(
            name=self.name,
            progress_status=_('In progress') if self.in_progress else _('Closed'),
            date_start=self.date_start,
            date_end=self.date_end
        )

    class Meta:
        verbose_name = _('Exam')
        verbose_name_plural = _('Exams')


class Task(models.Model):
    exam = models.ForeignKey(Exam)
    title = models.CharField(_('Title'), max_length=128)
    description = models.TextField(_('Description'))
    path = models.CharField(_('Source path'), max_length=256)
    runtime_env_group = models.ForeignKey('grader_environments.RuntimeEnvironmentGroup')

    def max_points(self):
        scenarios = self.scenario_set.all().aggregate(points=Sum('points'))
        return scenarios.get('points', 0)

    def __str__(self):
        return '{title} ({path})'.format(
            title=self.title,
            path=self.path
        )

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class Scenario(models.Model):
    TYPE_DIFF = 'diff'

    SCENARIO_TYPE_CHOICES = {
        TYPE_DIFF: 'Diff'
    }

    TYPE_HELP_TEXT = "Available scenario types:<br>" \
                     "Diff - a standard output comparison. This test looks at either stdout or stderr (or both). " \
                     "Can score either 0% or 100% available points."

    task = models.ForeignKey(Task)
    arguments = models.CharField(_('Arguments'), max_length=1024, null=True, blank=True)
    scenario_type = models.CharField(_('Type'), max_length=16, choices=list(SCENARIO_TYPE_CHOICES.items()),
                                     help_text=mark_safe(TYPE_HELP_TEXT))

    pattern_stdout = models.TextField(_('Expected standard output'), null=True, blank=True)
    pattern_stderr = models.TextField(_('Expected standard error output'), null=True, blank=True)
    points = models.IntegerField(_('Points for this scenario'), default=0)

    def __str__(self):
        return '{scenario_type} scenario for {task} (Score: {points}, args: {args})'.format(
            scenario_type=self.scenario_type,
            task=self.task,
            points=self.points,
            args=self.arguments
        )

    class Meta:
        verbose_name = _('Scenario')
        verbose_name_plural = _('Scenarios')
