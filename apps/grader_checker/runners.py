import logging
import threading

import os
import time

from apps.grader_core.models import Scenario
from apps.grader_environments.provisioning import GraderProvisioningManager
from apps.grader_environments.provisioning import TaskProvisioningManager
from .scenario_validators import DiffScenarioValidator


logger = logging.getLogger('grader')


class ScenarioRunner:
    SCENARIO_TYPE_MAP = {
        Scenario.TYPE_DIFF: DiffScenarioValidator
    }

    def __init__(self, scenario, user, executable, runtime_env):
        self.scenario = scenario
        self.user = user
        # self.base_path = base_path
        self.executable = executable
        self.runtime_env = runtime_env

    def run(self):
        logger.info('Running validator for scenario: %s', self.scenario)
        ssh_rpc_client = self.runtime_env.ssh_rpc_client
        validator_cls = self.SCENARIO_TYPE_MAP.get(self.scenario.scenario_type)
        validator = validator_cls(self.scenario, self.executable, self.user)

        grd_run_kwargs = validator.build_run_command()
        logger.debug('Running grd_run with following kwargs: %s', repr(grd_run_kwargs))
        results = ssh_rpc_client.grd_run(**grd_run_kwargs)
        validator.validate(results)
        logger.debug('Validator results: %s', repr(results))
        logger.info('User scored %d / %d', validator.points, self.scenario.points)


class RunnerThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.runtime_env = kwargs.pop('runtime_env')
        self.task_queue = kwargs.pop('task_queue')
        super().__init__(*args, **kwargs)
        logger.debug('Initialized thread <%s> for environment <%s>', self.name, self.runtime_env)

    def run(self):
        logger.debug('Running thread <%s>', self.name)
        while True:
            time.sleep(0.1)  # Sleep to make the whole thread a little less CPU consuming and easier to debug
            try:
                task = self.task_queue.pop()
            except IndexError:
                break

            user = task.get('user')
            executable = task.get('executable')
            base_path = task.get('base_path')

            logger.debug('Consumed a task for user `%s`', user)
            start = time.time()

            upload_files = [os.path.join(base_path, user, executable)]
            files_exist = True
            for file_path in upload_files:
                if not os.path.exists(file_path):
                    logger.info(
                        'Users file does not exist, skipping: {}'.format(
                            file_path
                        )
                    )
                    files_exist = False

            if not files_exist:
                continue

            manager = TaskProvisioningManager(runtime_env=self.runtime_env,
                                              files=[os.path.join(base_path, user, executable)])
            manager.provision()

            for scenario in task.get('scenarios'):
                logger.debug('Starting scenario %s', scenario)
                runner = ScenarioRunner(scenario, user, executable=executable, runtime_env=self.runtime_env)
                runner.run()

            end = time.time()
            logger.debug('Finished processing this task in %f seconds', end - start)

        logger.debug('Quitting, no more tasks found on the queue')
        return


class TaskRunner:
    def __init__(self, task, changed_files, repository_path):
        """
        A Runner class that searches for all scenarios related to a particular
        task and runs all of them.
        :param task: The task that will be checked
        :type task: apps.grader_core.models.Task
        """
        self.task = task
        self.repo = self.task.exam.repository
        self.changed_files = changed_files
        self.repository_path = repository_path
        # A queue holding up task batches, where each single batch can be run
        # independently
        self.task_queue = []
        self.environ_usage_info = {}

    def get_users(self):
        replace_repository_path = self.repository_path
        if not replace_repository_path.endswith('/'):
            replace_repository_path += '/'

        changed_files = map(
            lambda x: x.replace(replace_repository_path, ''),
            self.changed_files
        )
        users = [i.split('/')[0] for i in changed_files]
        users = [i for i in users if not i.startswith('.')]
        return list(set(users))

    def provision_task(self, user, base_path):
        manager = TaskProvisioningManager(runtime_env=self.task.runtime_env_group.runtimeenvironment_set.all()[0],
                                          files=[os.path.join(base_path, user, self.task.path)])
        manager.provision()

    def build_task_queue(self, users):
        for user in users:
            tb = {'user': user,
                  'executable': self.task.path,
                  'scenarios': [],
                  'base_path': self.repository_path}
            for scenario in self.task.scenario_set.all():
                tb['scenarios'].append(scenario)
            self.task_queue.append(tb)

    def run_tasks(self):
        environments = self.task.runtime_env_group.runtimeenvironment_set.all()
        logger.debug('Using %d runtime environments', environments.count())

        threads = []
        for env in environments:
            self.environ_usage_info[env] = False
            thr = RunnerThread(runtime_env=env, task_queue=self.task_queue)
            threads.append(thr)

        for thr in threads:
            thr.start()

        for thr in threads:
            thr.join()

        logger.debug('All threads have been joined, nothing more to do, quitting')

    def run(self):
        # TODO: repository handling instead of raw directory scan
        if self.task.scenario_set.count() == 0:
            logger.debug('Started TaskRunner for task: %s, but no scenarios have been found, discarding further checks',
                         self.task)
            return

        logger.debug('Started TaskRunner for task: %s', self.task)
        users = self.get_users()
        logger.debug('Users found: %d', len(users))

        provision_manager = GraderProvisioningManager(re_group=self.task.runtime_env_group)
        provision_manager.provision()
        self.build_task_queue(users)
        self.run_tasks()
        # self.run_task_for_users(users, self.repo.url)
        # self.close_all_ssh_connections()
