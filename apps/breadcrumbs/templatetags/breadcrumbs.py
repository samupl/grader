from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def breadcrumb(request, url, label, force_active=False):
    try:
        url = reverse(url)
    except NoReverseMatch:
        pass
    current_url = request.path

    current = False
    if force_active or url == current_url:
        current = True

    return render_to_string(
        template_name='breadcrumbs/breadcrumb.html',
        context={
            'label': label,
            'url': url,
            'current': current
        }
    )
