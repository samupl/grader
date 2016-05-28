from django.http import Http404
from django.shortcuts import render, get_object_or_404

from apps.grader_checker.models import LatestResult
from apps.grader_core.models import Exam


def exam_info(request, exam_id):
    """
    Exam information view, the exam 'Home page'

    :param int exam_id: Exam primary key
    :param django.http.request.HttpRequest request: Django Request object
    """

    exam = get_object_or_404(Exam, pk=exam_id)
    tasks = exam.task_set.all().prefetch_related('scenario_set')
    return render(request, 'frontend/exams/exam.html', {
        'exam': exam,
        'tasks': tasks
    })


def exam_scores_index(request, exam_id):
    """
    Exam scores index view

    :param int exam_id: Exam primary key
    :param django.http.request.HttpRequest request: Django Request object
    """
    exam = get_object_or_404(Exam, pk=exam_id)
    return render(request, 'frontend/exams/scores/index.html', {'exam': exam})


def exam_scores_single_index(request, exam_id):
    """
    Exam score by single user index page view

    :param int exam_id: Exam primary key
    :param django.http.request.HttpRequest request: Django Request object
    """
    exam = get_object_or_404(Exam, pk=exam_id)
    users = LatestResult.users_for_exam(exam)
    return render(request, 'frontend/exams/scores/single_user/index.html', {
        'exam': exam,
        'users': users
    })


def exam_scores_single_user(request, exam_id, username):
    """
    Exam score by single user, score page for specific username

    :param int exam_id: Exam primary key
    :param django.http.request.HttpRequest request: Django Request object
    :param str username: Username
    """
    exam = get_object_or_404(Exam, pk=exam_id)
    users = LatestResult.users_for_exam(exam)
    if username not in users:
        raise Http404

    task_results = LatestResult.get_results_for_user(exam, username)
    return render(request, 'frontend/exams/scores/single_user/single.html', {
        'exam': exam,
        'username': username,
        'task_results': task_results
    })


def exam_scores_all_users(request, exam_id):
    """
    Exam scores, list of all results for all users in a particular exam.

    :param int exam_id: Exam primary key
    :param django.http.request.HttpRequest request: Django Request object
    """
    exam = get_object_or_404(Exam, pk=exam_id)
    users = LatestResult.users_for_exam(exam)
    results = []
    for username in users:
        results.append({
            'user': username,
            'task_results': LatestResult.get_results_for_user(exam, username)
        })
    return render(request, 'frontend/exams/scores/all_users/index.html', {
        'exam': exam,
        'results': results
    })


def exam_scores_all_users_table(request, exam_id):
    """
    Exam scores, list of all results for all users in a particular exam.
    Tabular view.

    :param int exam_id: Exam primary key
    :param django.http.request.HttpRequest request: Django Request object
    """
    exam = get_object_or_404(Exam, pk=exam_id)
    tasks = exam.task_set.all().prefetch_related('scenario_set')
    users = LatestResult.users_for_exam(exam)
    results = []
    for username in users:
        results.append({
            'user': username,
            'task_results': LatestResult.get_results_for_user(exam, username)
        })
    return render(request, 'frontend/exams/scores/table_results/index.html', {
        'exam': exam,
        'results': results,
        'tasks': tasks
    })
