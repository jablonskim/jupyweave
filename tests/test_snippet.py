from unittest import TestCase
from snippet import Snippet, PATTERN_CODE_SNIPPET, GROUP_NAME__CODE

from exceptions.snippet_errors import BeginSnippetSyntaxError, EndSnippetSyntaxError

import json
import re


TEST_DATA_DIR = './test_data/snippets/'


class TestSnippet(TestCase):
    """Tests Snippet class (creation of regular expressions)"""

    def setUp(self):
        """Tests setup. Loads needed data."""

        with open(TEST_DATA_DIR + 'snippet_test_data.json') as f:
            self.snippet_data = json.load(f)

        with open(TEST_DATA_DIR + 'snippet_test_data_with_syntax_errors.json') as f:
            self.snippet_data_with_syntax = json.load(f)

        with open(TEST_DATA_DIR + 'snippets_example_with_patterns.html') as f:
            self.example_with_patterns = f.read()

        with open(TEST_DATA_DIR + 'snippets_example_without_patterns.html') as f:
            self.example_without_patterns = f.read()

        with open(TEST_DATA_DIR + 'end_pattern_search_result.txt') as f:
            self.end_pattern_search_result = f.read()

        with open(TEST_DATA_DIR + 'code_example.txt') as f:
            self.code_example = f.read()

    def test_create_end_pattern(self):
        """Tests creation of Snippet End pattern matching it with valid document"""
        end_pattern = Snippet.create_end_pattern(self.snippet_data)
        m = re.search(end_pattern, self.example_with_patterns)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(), self.end_pattern_search_result)

    def test_create_end_pattern_no_code(self):
        """Tests creation of Snippet End pattern on document without match"""
        end_pattern = Snippet.create_end_pattern(self.snippet_data)
        m = re.search(end_pattern, self.example_without_patterns)
        self.assertIsNone(m)

    def test_create_end_pattern_invalid_config(self):
        """Tests creation od Snippet End pattern on invalid configuration"""
        with self.assertRaises(EndSnippetSyntaxError):
            Snippet.create_end_pattern(self.snippet_data_with_syntax)

    def test_create_begin_pattern(self):
        """Tests creation of Snippet Begin pattern matching it with valid document"""
        self.fail()

    def test_create_begin_pattern_no_code(self):
        """Tests creation of Snippet Begin pattern on document without match"""
        self.fail()

    def test_create_begin_pattern_invalid_config(self):
        """Tests creation od Snippet Begin pattern on invalid configuration"""
        self.fail()

    def test_create_output_pattern(self):
        """Tests creation of Snippet Output pattern matching it with valid document"""
        self.fail()

    def test_create_output_pattern_no_code(self):
        """Tests creation of Snippet Output pattern on document without match"""
        self.fail()

    def test_create_output_pattern_invalid_config(self):
        """Tests creation od Snippet Output pattern on invalid configuration"""
        self.fail()

    def test_code_pattern(self):
        """Tests source code pattern"""
        m = re.search(PATTERN_CODE_SNIPPET, self.code_example)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(GROUP_NAME__CODE), self.code_example)

    def test_pattern_snippet(self):
        """Tests Begin-End snippet match"""
        self.fail()

    def test_pattern_output(self):
        """Tests Output snippet match"""
        self.fail()

    def test_pattern_no_match(self):
        """Test re witch no match"""
        self.fail()
