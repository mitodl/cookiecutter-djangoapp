"""Tests for URLs"""

from unittest import TestCase
from django.core.urlresolvers import reverse


class URLTests(TestCase):
    """URL tests"""

    def test_urls(self):
        """Make sure URLs match with resolved names"""
        assert reverse('{{ cookiecutter.project_name }}-index') == '/'
