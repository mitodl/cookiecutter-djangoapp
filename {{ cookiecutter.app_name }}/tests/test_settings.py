"""
Validate that our settings functions work, and we can create yaml files
"""
import os
import tempfile
import unittest

import mock
import yaml

from {{ cookiecutter.project_name }}.settings import load_fallback, get_var


class TestSettings(unittest.TestCase):
    """Validate that settings work as expected."""

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

    @mock.patch.dict('{{ cookiecutter.project_name }}.settings.FALLBACK_CONFIG', {'FOO': 'bar'})
    def test_get_var(self):
        """Verify that get_var does the right thing with precedence"""
        # Verify fallback
        self.assertEqual(get_var('FOO', 'notbar'), 'bar')

        # Verify default value
        self.assertEqual(get_var('NOTATHING', 'foobar'), 'foobar')

        # Verify environment variable wins:
        with mock.patch.dict(
            'os.environ', {'FOO': 'notbar'}, clear=True
        ):
            self.assertEqual(get_var('FOO', 'lemon'), 'notbar')
