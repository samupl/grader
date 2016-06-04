import shlex

import subprocess

import os
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest

from apps.api.tools import parse_grader_line


@login_required
@require_POST
@user_passes_test(lambda u: u.is_staff)
def get_scenario_info_from_executable(request):
    exec_str = request.POST.get('executable')
    if not exec_str:
        return HttpResponseBadRequest('No executable provided')

    exec_subprocess = shlex.split(exec_str)

    try:
        sp = subprocess.Popen(
            exec_subprocess,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except FileNotFoundError as e:
        return JsonResponse(data={'message': str(e)}, status=404)
    except PermissionError as e:
        return JsonResponse(data={'message': str(e)}, status=403)
    except OSError as e:
        return JsonResponse(data={'message': str(e)}, status=409)

    std_out, std_err = sp.communicate()

    return_code = sp.returncode
    str_std_out = std_out.decode(encoding='UTF-8')
    str_std_err = std_err.decode(encoding='UTF-8')

    std_out_lines = str_std_out.split(os.linesep, 1)
    if len(std_out_lines) < 1:
        return JsonResponse(
            data={
                'message': ugettext_lazy(
                    'The provided executable did not return enough lines of '
                    'output to stdout.'
                )
            },
            status=409
        )

    grader_line = std_out_lines[0]
    str_std_out = std_out_lines[1]
    grader_info = parse_grader_line(grader_line)

    if not grader_line.startswith('# grader: '):
        return JsonResponse(
            data={
                'message': ugettext_lazy(
                    'The provided executable did not return a valid grader '
                    'line.'
                )
            },
            status=409
        )

    return JsonResponse(data={
        'executable': exec_str,
        'subprocess_executable': exec_subprocess,
        'return_code': return_code,
        'std_out': str_std_out,
        'std_err': str_std_err,
        'grader_line': grader_line,
        'filename': grader_info.get('filename'),
        'arguments': grader_info.get('arguments'),
        'points': grader_info.get('points')
    })
