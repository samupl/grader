class BaseValidator:
    def __init__(self, scenario, executable, user):
        self.scenario = scenario
        self.executable = executable
        self.user = user

        self.std_out = None
        self.std_err = None

        self.points = None
        self.results = None

        self.additional_params = {
            'diff_stdout': '',
            'diff_stderr': ''
        }

    def validate(self, results):
        self.results = results
        # self.run_user_script()
        self.points = self.score()
        self.save_result()
        self.cleanup()

    # Methods that should be changed in child classes to alter the scenario scoring method
    def score(self):
        raise NotImplementedError

    def save_result(self):
        raise NotImplementedError

    def cleanup(self):
        pass

    def build_run_command(self):
        raise NotImplementedError
