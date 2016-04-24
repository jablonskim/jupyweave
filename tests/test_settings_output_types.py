from unittest import TestCase
from settings.output_types import OutputTypes


class TestOutputTypes(TestCase):

    def test_is_enabled(self):
        x = OutputTypes(None)

        self.assertTrue(x.is_enabled('stdout'))
        self.assertTrue(x.is_enabled('stderr'))
        self.assertTrue(x.is_enabled('text'))
        self.assertTrue(x.is_enabled('image'))
        self.assertFalse(x.is_enabled('invalid'))

        x = OutputTypes('All')

        self.assertTrue(x.is_enabled('stdout'))
        self.assertTrue(x.is_enabled('stderr'))
        self.assertTrue(x.is_enabled('text'))
        self.assertTrue(x.is_enabled('image'))
        self.assertFalse(x.is_enabled('invalid'))

        x = OutputTypes('Stdout, Image')

        self.assertTrue(x.is_enabled('stdout'))
        self.assertFalse(x.is_enabled('stderr'))
        self.assertFalse(x.is_enabled('text'))
        self.assertTrue(x.is_enabled('image'))
        self.assertFalse(x.is_enabled('invalid'))
