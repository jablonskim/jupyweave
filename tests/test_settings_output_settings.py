from copy import deepcopy
from unittest import TestCase

from jupyweave.exceptions import InvalidConfigurationError
from jupyweave.settings import OutputSettings


class TestOutputSettings(TestCase):

    DATA = {
        "results_base": "examples/outputs/",
        "filename": "{NAME}.{EXT}",
        "data_dir": "{NAME}_{EXT}_data",

        "patterns": {
            "name": "{NAME}",
            "extension": "{EXT}"
        }
    }

    def test_invalid_fields(self):
        invalid_data = deepcopy(TestOutputSettings.DATA)
        invalid_data['invalid'] = 'invalid'

        with self.assertRaises(InvalidConfigurationError):
            OutputSettings(invalid_data)

        invalid_data = deepcopy(TestOutputSettings.DATA)
        invalid_data['patterns']['invalid'] = 'invalid'

        with self.assertRaises(InvalidConfigurationError):
            OutputSettings(invalid_data)

    def test_data_directory(self):
        s = OutputSettings(TestOutputSettings.DATA)
        self.assertEqual('examples/outputs/test_txt_data', s.data_directory('test1/test2/test.txt'))

    def test_data_dir_url(self):
        s = OutputSettings(TestOutputSettings.DATA)
        self.assertEqual('test_txt_data', s.data_dir_url('test1/test2/test.txt'))

    def test_output_filename(self):
        s = OutputSettings(TestOutputSettings.DATA)
        self.assertEqual('examples/outputs/test.txt', s.output_filename('test1/test2/test.txt'))
