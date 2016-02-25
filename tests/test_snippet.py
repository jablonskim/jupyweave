from unittest import TestCase
from snippet import Snippet, PATTERN_CODE_SNIPPET
from snippet import GROUP_NAME__CODE, GROUP_NAME__LANGUAGE, GROUP_NAME__OUTPUT, \
    GROUP_NAME__ECHO, GROUP_NAME__CONTEXT, GROUP_NAME__ID

from exceptions.snippet_errors import BeginSnippetSyntaxError, EndSnippetSyntaxError, OutputSnippetSyntaxError

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

        with open(TEST_DATA_DIR + 'begin_pattern_search_results.txt') as f:
            self.begin_pattern_search_results = f.read()

        with open(TEST_DATA_DIR + 'output_pattern_search_results.txt') as f:
            self.output_pattern_search_results = f.read()

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
        begin_pattern = Snippet.create_begin_pattern(self.snippet_data)
        matches = re.finditer(begin_pattern, self.example_with_patterns)
        m = [match for match in matches]
        self.assertEqual(len(m), 2)

        self.assertIsNotNone(m[0])
        self.assertEqual(m[0].group(), self.begin_pattern_search_results[0])
        self.assertEqual(m[0].group(GROUP_NAME__LANGUAGE), self.begin_pattern_search_results[1])
        self.assertEqual(m[0].group(GROUP_NAME__OUTPUT), self.begin_pattern_search_results[2])
        self.assertEqual(m[0].group(GROUP_NAME__ECHO), self.begin_pattern_search_results[3])

        self.assertIsNotNone(m[1])
        self.assertEqual(m[1].group(), self.begin_pattern_search_results[4] + '\n' + self.begin_pattern_search_results[5])
        self.assertEqual(m[1].group(), self.begin_pattern_search_results[6])
        self.assertEqual(m[1].group(), self.begin_pattern_search_results[7])
        self.assertEqual(m[1].group(), self.begin_pattern_search_results[8])
        self.assertEqual(m[1].group(), self.begin_pattern_search_results[9])

    def test_create_begin_pattern_no_code(self):
        """Tests creation of Snippet Begin pattern on document without match"""
        begin_pattern = Snippet.create_begin_pattern(self.snippet_data)
        m = re.search(begin_pattern, self.example_without_patterns)
        self.assertIsNone(m)

    def test_create_begin_pattern_invalid_config(self):
        """Tests creation od Snippet Begin pattern on invalid configuration"""
        with self.assertRaises(BeginSnippetSyntaxError):
            Snippet.create_begin_pattern(self.snippet_data_with_syntax)

    def test_create_output_pattern(self):
        """Tests creation of Snippet Output pattern matching it with valid document"""
        output_pattern = Snippet.create_output_pattern(self.snippet_data)
        matches = re.finditer(output_pattern, self.example_with_patterns)
        m = [match for match in matches]
        self.assertEqual(len(m), 1)

        self.assertIsNotNone(m[0])
        self.assertEqual(m[0].group(), self.output_pattern_search_results[0] + '\n' + self.output_pattern_search_results[1])
        self.assertEqual(m[0].group(GROUP_NAME__ID), self.begin_pattern_search_results[2])

    def test_create_output_pattern_no_code(self):
        """Tests creation of Snippet Output pattern on document without match"""
        output_pattern = Snippet.create_output_pattern(self.snippet_data)
        m = re.search(output_pattern, self.example_without_patterns)
        self.assertIsNone(m)

    def test_create_output_pattern_invalid_config(self):
        """Tests creation od Snippet Output pattern on invalid configuration"""
        with self.assertRaises(OutputSnippetSyntaxError):
            Snippet.create_output_pattern(self.snippet_data_with_syntax)

    def test_code_pattern(self):
        """Tests source code pattern"""
        m = re.search(PATTERN_CODE_SNIPPET, self.code_example)
        self.assertIsNotNone(m)
        self.assertEqual(m.group(GROUP_NAME__CODE), self.code_example)

    def test_pattern_snippet(self):
        """Tests Begin-End snippet match"""
        # TODO
        self.fail()

    def test_pattern_output(self):
        """Tests Output snippet match"""
        # TODO
        self.fail()

    def test_pattern_no_match(self):
        """Test re witch no match"""
        # TODO
        self.fail()
