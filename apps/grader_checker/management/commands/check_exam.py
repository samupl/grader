import logging

import os
from django.conf import settings
from django.core.management import BaseCommand, CommandError

from apps.grader_checker.runners import TaskRunner
from apps.grader_core.models import Exam
from apps.grader_core.repository_providers.registry import registry


logger = logging.getLogger('grader')


class Command(BaseCommand):
    help = 'Checks all tasks for each user in the specified exam'

    def add_arguments(self, parser):
        parser.add_argument('exam_id', type=str)

    def handle(self, *args, **options):
        exam_id = options.get('exam_id')
        try:
            exam = Exam.objects.get(name=exam_id)
        except Exam.DoesNotExist:
            raise CommandError('Exam `{}` does not exist.'.format(exam_id))

        tasks = exam.task_set.all()
        # Repository handling
        logger.info('Checking for changes in repository')
        repository_path = os.path.join(
            settings.BASE_DIR,
            'repositories',
            exam.repository.repository_id
        )
        repository_handler_cls = registry.get(exam.repository.repository_type)
        repository_handler = repository_handler_cls(
            exam.repository.url,
            repository_path
        )
        if not os.path.exists(repository_path):
            logger.info(
                'Repository is being checked out for the first time. '
                'All files within this repository will be checked.'
            )
            rev_num = repository_handler.checkout()
            logger.debug('Current revision: {}'.format(rev_num))
            changed_files = repository_handler.changed_files(rev_num)
        else:
            previous_rev_num = repository_handler.current_revision()
            rev_num = repository_handler.update()
            if rev_num:
                logger.debug('Current revision: {}'.format(rev_num))
            else:
                logger.info('No updates on the remote repository')
                return
            changed_files = repository_handler.changed_files(
                rev_num, previous_rev_num
            )

        for t in tasks:
            runner = TaskRunner(
                task=t,
                changed_files=changed_files,
                repository_path=repository_path
            )
            runner.run()
