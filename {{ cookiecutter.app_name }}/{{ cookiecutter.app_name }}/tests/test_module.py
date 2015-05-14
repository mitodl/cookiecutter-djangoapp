# -*- coding: utf-8 -*-
"""
Testing of the module level stuff itself
"""
import unittest

import semantic_version


class TestModule(unittest.TestCase):
    """
    Test core module features, like asserting the version
    and making sure we are exposing our classes.
    """

    @staticmethod
    def test_version():
        """
        Verify we have a valid semantic version
        """
        import {{ cookiecutter.app_name }}
        semantic_version.Version({{ cookiecutter.app_name }}.__version__)
