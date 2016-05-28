import datetime

from django.test import SimpleTestCase

from apps.grader_core.models import Exam


class ExamModelCase(SimpleTestCase):

    def test_in_progress_property_working(self):
        """ If current date is between exams start and end date, the property should return True """
        now = datetime.datetime.now()
        date_start = now - datetime.timedelta(hours=1)
        date_end = now + datetime.timedelta(hours=1)
        exam = Exam(
            date_start=date_start,
            date_end=date_end
        )
        self.assertTrue(exam.in_progress)

    def test_in_progress_property_after(self):
        """ If current date is between exams start and end date, the property should return True """
        now = datetime.datetime.now()
        date_start = now - datetime.timedelta(hours=2)
        date_end = now - datetime.timedelta(hours=1)
        exam = Exam(
            date_start=date_start,
            date_end=date_end
        )
        self.assertFalse(exam.in_progress)

    def test_in_progress_property_before(self):
        """ If current date is between exams start and end date, the property should return True """
        now = datetime.datetime.now()
        date_start = now + datetime.timedelta(hours=2)
        date_end = now + datetime.timedelta(hours=1)
        exam = Exam(
            date_start=date_start,
            date_end=date_end
        )
        self.assertFalse(exam.in_progress)
