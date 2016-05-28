from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from apps.grader_checker.models import Result
from apps.grader_core.models import Exam, Task, Scenario


def home(request):
    """
    A view for Grader home page

    :param request: Django Request object
    :type request: django.http.request.HttpRequest
    """
    now = timezone.now()

    current_filter = {'date_start__lte': now, 'date_end__gt': now}

    current_exams = Exam.objects.filter(**current_filter)
    archival_exams = Exam.objects.exclude(**current_filter)

    return render(request, 'frontend/index.html', {
        'current_exams': current_exams,
        'archival_exams': archival_exams
    })


def javascript(request):
    """
    A view for translated javascript constants, such as translations and urls

    :param request: Django Request object
    :type request: django.http.request.HttpRequest
    """
    return render(request, 'frontend/javascript.js', content_type='text/javascript')


def statistics(request):
    """
    A JSON response view that returns basic statistics, used by the home page

    :param request: Django Request object
    :type request: django.http.request.HttpRequest
    """
    data = dict()

    data['exams'] = Exam.objects.count()
    data['results'] = Result.objects.count()
    data['tasks'] = Task.objects.count()
    data['scenarios'] = Scenario.objects.count()

    return JsonResponse(data)
