from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from apps.grader_core.models import Exam


@login_required
@require_POST
@user_passes_test(lambda u: u.is_staff)
def change_exam_desc(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    desc = request.POST['content']
    exam.description = desc
    exam.save()
    return JsonResponse({'status': True})
