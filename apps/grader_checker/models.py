from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.grader_core.models import Scenario


class Result(models.Model):
    check_date = models.DateTimeField(_('Check date'), auto_now_add=True)
    points = models.IntegerField(_('Scored points'), default=0)
    user = models.CharField(_('User'), max_length=128)
    scenario = models.ForeignKey(Scenario)
    std_out = models.TextField()
    std_err = models.TextField()
    diff_stdout = models.TextField()
    diff_stderr = models.TextField()


class LatestResult(models.Model):
    check_date = models.DateTimeField(_('Check date'), auto_now_add=True)
    points = models.IntegerField(_('Scored points'), default=0)
    user = models.CharField(_('User'), max_length=128)
    scenario = models.ForeignKey(Scenario)
    std_out = models.TextField()
    std_err = models.TextField()
    diff_stdout = models.TextField()
    diff_stderr = models.TextField()

    @classmethod
    def users_for_exam(cls, exam):
        """
        Get a list of users for a specific exam

        :param apps.grader_core.models.Exam exam: Exam model instance
        """
        users = cls.objects.filter(
            scenario__task__exam=exam
        ).values('user').distinct()
        user_list = [u.get('user') for u in users]
        return user_list

    @classmethod
    def get_latest_for_user(cls, exam, username):
        results = cls.objects.filter(
            user=username,
            scenario__task__exam=exam
        ).select_related()
        return list(results)

    @classmethod
    def get_results_for_user(cls, exam, username):
        results = cls.get_latest_for_user(exam, username)
        tasks = exam.task_set.all().select_related().prefetch_related(
            'scenario_set')
        task_results = []
        for task in tasks:
            task_scenario_results = list(filter(
                lambda r: r.scenario.task == task, results
            ))
            task_result = {
                'task': task,
                'results': task_scenario_results,
                'points': sum([r.points for r in task_scenario_results]),
                'max_points': sum([s.points for s in task.scenario_set.all()]),
            }
            task_result['passed'] = task_result['points'] == task_result[
                'max_points'
            ]
            task_results.append(task_result)
        return task_results

    @property
    def passed(self):
        return self.points == self.scenario.points

    def __str__(self):
        return 'user={user}, scenario={scenario}'.format(
            user=self.user,
            scenario=self.scenario.pk
        )

    class Meta:
        ordering = ['user']
