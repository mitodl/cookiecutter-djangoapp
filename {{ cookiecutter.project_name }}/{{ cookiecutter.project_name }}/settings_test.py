"""
Validate that our settings functions work, and we can create yaml files
"""

import importlib
import os
import sys
import tempfile
from unittest import mock

from django.conf import settings
from django.core import mail
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
import semantic_version
import yaml

from {{ cookiecutter.project_name }}.settings import load_fallback, get_var


class TestSettings(TestCase):
    """Validate that settings work as expected."""

    def reload_settings(self):
        """
        Reload settings module with cleanup to restore it.

        Returns:
            dict: dictionary of the newly reloaded settings ``vars``
        """
        importlib.reload(sys.modules['{{ cookiecutter.project_name }}.settings'])
        # Restore settings to original settings after test
        self.addCleanup(importlib.reload, sys.modules['{{ cookiecutter.project_name }}.settings'])
        return vars(sys.modules['{{ cookiecutter.project_name }}.settings'])

    def test_load_fallback(self):
        """Verify our YAML load works as expected."""
        config_settings = {'TEST_KEY': 'yessir'}
        _, temp_config_path = tempfile.mkstemp()
        self.addCleanup(os.remove, temp_config_path)
        with open(temp_config_path, 'w') as temp_config:
            temp_config.write(yaml.dump(config_settings))

        with mock.patch('{{ cookiecutter.project_name }}.settings.CONFIG_PATHS') as config_paths:
            config_paths.__iter__.return_value = [temp_config_path]
            fallback_config = load_fallback()
            self.assertDictEqual(fallback_config, config_settings)

    def test_get_var(self):
        """Verify that get_var does the right thing with precedence"""
        with mock.patch.dict(
            '{{ cookiecutter.project_name }}.settings.FALLBACK_CONFIG',
            {'FOO': 'bar'}
        ):
            # Verify fallback
            self.assertEqual(get_var('FOO', 'notbar'), 'bar')

        # Verify default value
        self.assertEqual(get_var('NOTATHING', 'foobar'), 'foobar')

        # Verify environment variable wins:
        with mock.patch.dict(
            'os.environ', {'FOO': 'notbar'}, clear=True
        ):
            self.assertEqual(get_var('FOO', 'lemon'), 'notbar')

        # Verify that types work:
        with mock.patch.dict(
            'os.environ',
            {
                'FOO': 'False',
                'BAR': '[1,2,3]',
            },
            clear=True
        ):
            self.assertFalse(get_var('FOO', True))
            self.assertEqual(get_var('BAR', []), [1, 2, 3])
        # Make sure real types still work too (i.e. from yaml load)
        with mock.patch.dict(
            '{{ cookiecutter.project_name }}.settings.FALLBACK_CONFIG',
            {'BLAH': True}
        ):
            self.assertEqual(get_var('BLAH', False), True)

    def test_s3_settings(self):
        """Verify that we enable and configure S3 with a variable"""
        # Unset, we don't do S3
        with mock.patch.dict('os.environ', {
            '{{ cookiecutter.project_name|upper }}_USE_S3': 'False'
        }, clear=True):
            settings_vars = self.reload_settings()
            self.assertNotEqual(
                settings_vars.get('DEFAULT_FILE_STORAGE'),
                'storages.backends.s3boto.S3BotoStorage'
            )

        with self.assertRaises(ImproperlyConfigured):
            with mock.patch.dict('os.environ', {
                '{{ cookiecutter.project_name|upper }}_USE_S3': 'True',
            }, clear=True):
                self.reload_settings()

        # Verify it all works with it enabled and configured 'properly'
        with mock.patch.dict('os.environ', {
            '{{ cookiecutter.project_name|upper }}_USE_S3': 'True',
            'AWS_ACCESS_KEY_ID': '1',
            'AWS_SECRET_ACCESS_KEY': '2',
            'AWS_STORAGE_BUCKET_NAME': '3',
        }, clear=True):
            settings_vars = self.reload_settings()
            self.assertEqual(
                settings_vars.get('DEFAULT_FILE_STORAGE'),
                'storages.backends.s3boto.S3BotoStorage'
            )

    def test_admin_settings(self):
        """Verify that we configure email with environment variable"""

        with mock.patch.dict('os.environ', {
            '{{ cookiecutter.project_name|upper }}_ADMIN_EMAIL': ''
        }, clear=True):
            settings_vars = self.reload_settings()
            self.assertFalse(settings_vars.get('ADMINS', False))

        test_admin_email = 'cuddle_bunnies@example.com'
        with mock.patch.dict('os.environ', {
            '{{ cookiecutter.project_name|upper }}_ADMIN_EMAIL': test_admin_email,
        }, clear=True):
            settings_vars = self.reload_settings()
            self.assertEqual(
                (('Admins', test_admin_email),),
                settings_vars['ADMINS']
            )
        # Manually set ADMIN to our test setting and verify e-mail
        # goes where we expect
        settings.ADMINS = (('Admins', test_admin_email),)
        mail.mail_admins('Test', 'message')
        self.assertIn(test_admin_email, mail.outbox[0].to)

    def test_db_ssl_enable(self):
        """Verify that we can enable/disable database SSL with a var"""

        # Check default state is SSL on
        with mock.patch.dict('os.environ', {
            '{{ cookiecutter.project_name|upper }}_DB_DISABLE_SSL': ''
        }, clear=True):
            settings_vars = self.reload_settings()
            self.assertEqual(
                settings_vars['DATABASES']['default']['OPTIONS'],
                {'sslmode': 'require'}
            )

        # Check enabling the setting explicitly
        with mock.patch.dict('os.environ', {
            '{{ cookiecutter.project_name|upper }}_DB_DISABLE_SSL': 'True'
        }, clear=True):
            settings_vars = self.reload_settings()
            self.assertEqual(
                settings_vars['DATABASES']['default']['OPTIONS'],
                {}
            )

        # Disable it
        with mock.patch.dict('os.environ', {
            '{{ cookiecutter.project_name|upper }}_DB_DISABLE_SSL': 'False'
        }, clear=True):
            settings_vars = self.reload_settings()
            self.assertEqual(
                settings_vars['DATABASES']['default']['OPTIONS'],
                {'sslmode': 'require'}
            )

    @staticmethod
    def test_semantic_version():
        """
        Verify that we have a semantic compatible version.
        """
        semantic_version.Version(settings.VERSION)
