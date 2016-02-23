from unittest import TestCase
from snippet import Snippet, PATTERN_CODE_SNIPPET, GROUP_NAME__CODE

import json
import re


TEST_DATA_DIR = './test_data/snippets/'


class TestSnippet(TestCase):

    def setUp(self):
        with open(TEST_DATA_DIR + 'snippet_test_data.json') as f:
            self.snippet_data = json.load(f)

        with open(TEST_DATA_DIR + 'snippets_example_with_patterns.html') as f:
            self.example_with_patterns = f.read()

        with open(TEST_DATA_DIR + 'snippets_example_without_patterns.html') as f:
            self.example_without_patterns = f.read()

        with open(TEST_DATA_DIR + 'end_pattern_search_result.txt') as f:
            self.end_pattern_search_result = f.read()

        with open(TEST_DATA_DIR + 'code_example.txt') as f:
            self.code_example = f.read()

    def test_create_end_pattern(self):
        end_pattern = Snippet.create_end_pattern(self.snippet_data)
        m = re.search(end_pattern, self.example_with_patterns)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(), self.end_pattern_search_result)

    def test_create_end_pattern_no_code(self):
        end_pattern = Snippet.create_end_pattern(self.snippet_data)
        m = re.search(end_pattern, self.example_without_patterns)
        self.assertIsNone(m)

    def test_create_begin_pattern(self):
        self.fail()

    def test_create_output_pattern(self):
        self.fail()

    def test_code_pattern(self):
        m = re.search(PATTERN_CODE_SNIPPET, self.code_example)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(GROUP_NAME__CODE), self.code_example)

    def test_pattern(self):
        self.fail()
