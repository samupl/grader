import unittest

from apps.api.tools import parse_grader_line


class ParseGraderLineTestCase(unittest.TestCase):
    LINE_VALID = (
        "# grader:  /home/js/Studia/praca_dyplomowa/grader/home/js/test.sh "
        "-a -b -c 1 2 3 4 5 -- 100"
    )
    LINE_VALID_NO_ARGS = (
        "# grader:  /home/js/Studia/praca_dyplomowa/grader/home/js/test.sh "
        "-- 100"
    )

    def test_line_valid_filename(self):
        info = parse_grader_line(self.LINE_VALID)
        self.assertEqual(
            info['filename'],
            '/home/js/Studia/praca_dyplomowa/grader/home/js/test.sh'
        )

    def test_line_valid_arguments(self):
        info = parse_grader_line(self.LINE_VALID)
        self.assertEqual(
            info['arguments'],
            '-a -b -c 1 2 3 4 5'
        )

    def test_line_valid_points(self):
        info = parse_grader_line(self.LINE_VALID)
        self.assertEqual(
            info['points'],
            100
        )

    def test_line_valid2_filename(self):
        info = parse_grader_line(self.LINE_VALID_NO_ARGS)
        self.assertEqual(
            info['filename'],
            '/home/js/Studia/praca_dyplomowa/grader/home/js/test.sh'
        )

    def test_line_valid2_arguments(self):
        info = parse_grader_line(self.LINE_VALID_NO_ARGS)
        self.assertEqual(
            info['arguments'],
            ''
        )

    def test_line_valid2_points(self):
        info = parse_grader_line(self.LINE_VALID_NO_ARGS)
        self.assertEqual(
            info['points'],
            100
        )
