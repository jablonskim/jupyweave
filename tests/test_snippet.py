from unittest import TestCase
from snippet import Snippet, PATTERN_CODE_SNIPPET

import re


class TestSnippet(TestCase):

    def setUp(self):
        self.code_example = "for i in range(5):\n\tprint(i)"

    def test_create_end_pattern(self):
        self.fail()

    def test_create_begin_pattern(self):
        self.fail()

    def test_create_output_pattern(self):
        self.fail()

    def test_code_pattern(self):
        m = re.search(PATTERN_CODE_SNIPPET, self.code_example)
        self.assertIsNotNone(m)
        self.assertEqual(m.group('code'), self.code_example)

    def test_pattern(self):
        self.fail()
