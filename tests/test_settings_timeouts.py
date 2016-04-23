from unittest import TestCase
from settings.timeouts import Timeouts
from exceptions.settings_errors import InvalidConfigurationError


class TestTimeouts(TestCase):

    DATA = {
        "default": 1000,
        "languages": {
            "Language 1": 500,
            "Language 2": 10000
        }
    }

    def test_timeouts(self):
        timeouts = Timeouts(TestTimeouts.DATA)

        self.assertEqual(10000, timeouts.timeout('Language 2'))
        self.assertEqual(1000, timeouts.timeout('Language 3'))

    def test_invalid_data(self):
        with self.assertRaises(InvalidConfigurationError):
            Timeouts({})

    def test_invalid_numbers(self):
        with self.assertRaises(InvalidConfigurationError):
            Timeouts({
                "default": "1000"
            })

        with self.assertRaises(InvalidConfigurationError):
            Timeouts({
                "default": 1000,
                "languages": {"aa": "122"}
            })

        with self.assertRaises(InvalidConfigurationError):
            Timeouts({
                "default": 1000,
                "languages": {"aa": "10q"}
            })

    def test_invalid_fields(self):
        with self.assertRaises(InvalidConfigurationError):
            Timeouts({
                "default": 1000,
                "languages": {},
                "invalid": "invalid"
            })
