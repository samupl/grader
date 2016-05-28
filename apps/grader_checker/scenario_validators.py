import difflib
import shlex

from apps.grader_checker.models import Result, LatestResult
from .base import BaseValidator


class DiffScenarioValidator(BaseValidator):
    def score(self):
        self.std_out = self.results.get('stdout')
        self.std_err = self.results.get('stderr')

        output_stdout = self.std_out.splitlines()
        expected_output = self.scenario.pattern_stdout.splitlines()

        diff_stdout = '\n'.join(difflib.unified_diff(output_stdout, expected_output))
        self.additional_params['diff_stdout'] = diff_stdout

        output_stderr = self.std_err.splitlines()
        expected_output = self.scenario.pattern_stderr.splitlines()

        diff_stderr = '\n'.join(difflib.unified_diff(output_stderr, expected_output))
        self.additional_params['diff_stderr'] = diff_stderr

        if not bool(diff_stdout) and not(bool(diff_stderr)):
            return self.scenario.points
        else:
            return 0

    def save_result(self):
        result_kwargs = {
            'scenario': self.scenario,
            'points': self.points,
            'std_out': self.std_out,
            'std_err': self.std_err,
            'diff_stdout': self.additional_params['diff_stdout'],
            'diff_stderr': self.additional_params['diff_stderr'],
            'user': self.user
        }

        # Create a Result entry
        Result.objects.create(**result_kwargs)

        # Purge all LatestResults
        LatestResult.objects.filter(
            scenario=self.scenario,
            user=self.user
        ).delete()

        # Create latest result
        LatestResult.objects.create(**result_kwargs)

    def build_run_command(self):
        command = ['./' + self.executable]
        if self.scenario.arguments:
            command += shlex.split(self.scenario.arguments)
        return {'command': command}
