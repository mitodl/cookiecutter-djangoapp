"""Tests for URLs"""

from unittest import TestCase
from django.core.urlresolvers import reverse


class URLTests(TestCase):
    """URL tests"""

    def test_urls(self):
        """Make sure URLs match with resolved names"""
        import pdb; pdb.set_trace()
        assert reverse('ui-500') == "/500/"
        assert reverse('ui-404') == "/404/"
        assert reverse('{{ cookiecutter.project_name }}-index') == '/'
