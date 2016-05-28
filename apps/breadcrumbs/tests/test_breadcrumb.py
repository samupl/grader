import unittest
from unittest import mock

from django.core.urlresolvers import NoReverseMatch

from apps.breadcrumbs.templatetags.breadcrumbs import breadcrumb

url_patterns = {
    'frontend:home': '/'
}


class RequestMock:
    def __init__(self, path):
        self.path = path


def mocked_reverse(viewname):
    if viewname not in url_patterns:
        raise NoReverseMatch
    return url_patterns.get(viewname)


def mocked_render_to_string(template_name, context):
    context.update({'__template_name': template_name})
    return context


@mock.patch('apps.breadcrumbs.templatetags.breadcrumbs.reverse',
            new=mocked_reverse)
@mock.patch('apps.breadcrumbs.templatetags.breadcrumbs.render_to_string',
            new=mocked_render_to_string)
class BreadcrumbCase(unittest.TestCase):

    def test_breadcrumb_home_page(self):
        request = RequestMock(path='/')
        result = breadcrumb(request, 'frontend:home', 'Test')
        self.assertEqual(result, {
            '__template_name': 'breadcrumbs/breadcrumb.html',
            'label': 'Test',
            'url': '/',
            'current': True
        })

    def test_breadcrumb_other_than_home_page(self):
        request = RequestMock(path='/xxx')
        result = breadcrumb(request, 'frontend:home', 'Test')
        self.assertEqual(result, {
            '__template_name': 'breadcrumbs/breadcrumb.html',
            'label': 'Test',
            'url': '/',
            'current': False
        })

    def test_breadcrumb_nonexistent_page(self):
        request = RequestMock(path='/xxx')
        result = breadcrumb(request, 'test', 'Test')
        self.assertEqual(result, {
            '__template_name': 'breadcrumbs/breadcrumb.html',
            'label': 'Test',
            'url': 'test',
            'current': False
        })

    def test_breadcrumb_force_home_page(self):
        request = RequestMock(path='/')
        result = breadcrumb(request, 'frontend:home', 'Test',
                            force_active=True)
        self.assertEqual(result, {
            '__template_name': 'breadcrumbs/breadcrumb.html',
            'label': 'Test',
            'url': '/',
            'current': True
        })

    def test_breadcrumb_force_other_than_home_page(self):
        request = RequestMock(path='/xxx')
        result = breadcrumb(request, 'frontend:home', 'Test',
                            force_active=True)
        self.assertEqual(result, {
            '__template_name': 'breadcrumbs/breadcrumb.html',
            'label': 'Test',
            'url': '/',
            'current': True
        })
