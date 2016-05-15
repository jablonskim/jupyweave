from unittest import TestCase

from jupyweave.exceptions import InvalidConfigurationError
from jupyweave.settings.validator import Validator


class TestValidator(TestCase):

    def test_check_keys(self):
        Validator.check_keys({}, [], '')
        Validator.check_keys({}, ['a'], '')
        Validator.check_keys({'bb': 1, 'cc': 2}, ['a', 'b', 'bb', 'q', 'cc'], '')
        Validator.check_keys({'bb': 8, 'cc': 2}, ['bb', 'cc'], '')

        with self.assertRaises(InvalidConfigurationError):
            Validator.check_keys({'q': 7}, ['a', 'b', 'c'], '')
