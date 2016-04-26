from unittest import TestCase
from copy import deepcopy
from settings.snippet import Snippet
from settings.group_names import GroupName
from exceptions.settings_errors import InvalidConfigurationError
from exceptions.processor_errors import InvalidBoolValueError, TimeoutValueError


class TestSnippetPattern(TestCase):

    EXAMPLE2 = """<!DOCTYPE html>
<snippets_settings lang="Python 3" />
<html>
<body>

    <p>This is a paragraph.</p>
    <snippet output="T" timeout="20000" echo="True" output_type="All" processor="highlight" lines="6-11,13">
%matplotlib inline
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**2

x = np.linspace(0, 3*np.pi, 500)
plt.plot(x, np.sin(f(x)))
plt.title('A simple chirp')
print('before')
plt.show()
print('after')
    </snippet>
    <p>This is a paragraph.</p>
    <p>This is a paragraph.</p>
    <p>This is a paragraph.</p>
    <p>This is a paragraph.</p>
    <div></div>
    <snippet lang="Python 3"    output="F" context="TestCtx2" allow_error="F" processor="highlight"
             id="test_id1">
for i in range(5):
    print(i)

j = 100
j
    </snippet>
    <p>This is a paragraph.</p>
    <p><output
            id="test_id1" /></p>
    <p>This is a paragraph.</p>
    <p>This is a paragraph.</p>
    <b>ąłńżźćęóążź</b>
    <snippet lang="SQL" lines="!1">
        !sqlite:///:memory:;
        CREATE TABLE test (id, aa, bb);
        INSERT INTO test VALUES (1, 'test1', 'test2');
        INSERT INTO test VALUES (2, 'test2', 'test2');
        SELECT * FROM test;
        SELECT 5;
        DELETE FROM test WHERE id = 2;
        SELECT * FROM test;
    </snippet>

</body>
</html>"""

    EXAMPLE1 = """Markdown example
================

Testtesttest
------------

1. Test test

Te*s*t

<#[Python 3] echo=T output=T>
for i in range(10):
    print(i)

print('Test')
<@>

T**es**t

> qqq

> qqq

Link [example](https://pl.wikipedia.org/wiki/Markdown)

Test `Test` Test

"""

    DATA1 = {
        "begin": "<#{S}>",
        "end": "<@>",
        "output": "<${S}>",
        "default_settings": "<!!!{S}>",

        "settings": {
            "language": "[{L}]",
            "echo": "echo={E}",
            "output": "output={O}",
            "context": "context={C}",
            "snippet_id": "id={I}",
            "timeout": "timeout={T}",
            "error": "allow_error={R}",
            "output_type": "output_type={OT}",
            "processor": "processor={P}",
            "echo_lines": "lines={EL}"
        },

        "patterns": {
            "settings": "{S}",
            "language": "{L}",
            "echo": "{E}",
            "output": "{O}",
            "context": "{C}",
            "snippet_id": "{I}",
            "timeout": "{T}",
            "error": "{R}",
            "output_type": "{OT}",
            "processor": "{P}",
            "echo_lines": "{EL}"
        }
    }

    DATA2 = {
        "begin": "<snippet{S}>",
        "end": "</snippet>",
        "output": "<output{S}/>",
        "default_settings": "<snippets_settings{S}/>",

        "settings": {
            "language": "lang=\"{L}\"",
            "echo": "echo=\"{E}\"",
            "output": "output=\"{O}\"",
            "context": "context=\"{C}\"",
            "snippet_id": "id=\"{I}\"",
            "timeout": "timeout=\"{T}\"",
            "error": "allow_error=\"{R}\"",
            "output_type": "output_type=\"{OT}\"",
            "processor": "processor=\"{P}\"",
            "echo_lines": "lines=\"{EL}\""
        },

        "patterns": {
            "settings": "{S}",
            "language": "{L}",
            "echo": "{E}",
            "output": "{O}",
            "context": "{C}",
            "snippet_id": "{I}",
            "timeout": "{T}",
            "error": "{R}",
            "output_type": "{OT}",
            "processor": "{P}",
            "echo_lines": "{EL}"
        }
    }

    def test_invalid_fields(self):
        invalid_data = deepcopy(TestSnippetPattern.DATA1)
        invalid_data['invalid'] = 'invalid'

        with self.assertRaises(InvalidConfigurationError):
            Snippet(invalid_data)

        invalid_data = deepcopy(TestSnippetPattern.DATA1)
        invalid_data['settings']['invalid'] = 'invalid'

        with self.assertRaises(InvalidConfigurationError):
            Snippet(invalid_data)

        invalid_data = deepcopy(TestSnippetPattern.DATA1)
        invalid_data['patterns']['invalid'] = 'invalid'

        with self.assertRaises(InvalidConfigurationError):
            Snippet(invalid_data)

    def test_entry1(self):
        snippet = Snippet(TestSnippetPattern.DATA1)
        self.fail()

    def test_entry2(self):
        snippet = Snippet(TestSnippetPattern.DATA2)
        entry = snippet.pattern().entry()
        entries = [x for x in entry.finditer(TestSnippetPattern.EXAMPLE2)]

        self.assertEqual(4, len(entries))

        entry = entries[0]
        self.assertNotEqual(None, entry.group(GroupName.CODE_SNIPPET))
        self.assertEqual(None, entry.group(GroupName.OUTPUT_SNIPPET))
        self.assertNotEqual(None, entry.group(GroupName.CODE))

        code = """
%matplotlib inline
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**2

x = np.linspace(0, 3*np.pi, 500)
plt.plot(x, np.sin(f(x)))
plt.title('A simple chirp')
print('before')
plt.show()
print('after')
    """

        self.assertEqual(code, entry.group(GroupName.CODE))

        settings = ''' output="T" timeout="20000" echo="True" output_type="All" processor="highlight" lines="6-11,13"'''

        self.assertEqual(settings, entry.group(GroupName.CODE_SETTINGS))

        entry = entries[1]
        self.assertNotEqual(None, entry.group(GroupName.CODE_SNIPPET))
        self.assertEqual(None, entry.group(GroupName.OUTPUT_SNIPPET))
        self.assertNotEqual(None, entry.group(GroupName.CODE))

        code = """
for i in range(5):
    print(i)

j = 100
j
    """

        self.assertEqual(code, entry.group(GroupName.CODE))

        settings = ''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" processor="highlight"
             id="test_id1"'''

        self.assertEqual(settings, entry.group(GroupName.CODE_SETTINGS))

        entry = entries[2]
        self.assertEqual(None, entry.group(GroupName.CODE_SNIPPET))
        self.assertNotEqual(None, entry.group(GroupName.OUTPUT_SNIPPET))
        self.assertEqual(None, entry.group(GroupName.CODE))

        settings = '''
            id="test_id1" '''

        self.assertEqual(settings, entry.group(GroupName.OUTPUT_SETTINGS))

        entry = entries[3]
        self.assertNotEqual(None, entry.group(GroupName.CODE_SNIPPET))
        self.assertEqual(None, entry.group(GroupName.OUTPUT_SNIPPET))
        self.assertNotEqual(None, entry.group(GroupName.CODE))

        code = """
        !sqlite:///:memory:;
        CREATE TABLE test (id, aa, bb);
        INSERT INTO test VALUES (1, 'test1', 'test2');
        INSERT INTO test VALUES (2, 'test2', 'test2');
        SELECT * FROM test;
        SELECT 5;
        DELETE FROM test WHERE id = 2;
        SELECT * FROM test;
    """

        self.assertEqual(code, entry.group(GroupName.CODE))

        settings = ''' lang="SQL" lines="!1"'''

        self.assertEqual(settings, entry.group(GroupName.CODE_SETTINGS))

    def test_default_settings1(self):
        snippet = Snippet(TestSnippetPattern.DATA1)
        self.fail()

    def test_default_settings2(self):
        snippet = Snippet(TestSnippetPattern.DATA2)
        entry = snippet.pattern().default_settings()
        entries = [x for x in entry.finditer(TestSnippetPattern.EXAMPLE2)]

        self.assertEqual(1, len(entries))

        entry = entries[0]

        self.assertNotEqual(None, entry.group(GroupName.DEFAULT_SETTINGS_SNIPPET))

        settings = ''' lang="Python 3" '''

        self.assertEqual(settings, entry.group(GroupName.DEFAULT_SETTINGS))

    def test_language1(self):
        snippet = Snippet(TestSnippetPattern.DATA1)
        self.fail()

    def test_language2(self):
        snippet = Snippet(TestSnippetPattern.DATA2)

        self.assertEqual('Python 3', snippet.pattern().language(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" processor="highlight"
             id="test_id1"'''))

        self.assertEqual(None, snippet.pattern().language(''' aalang="Python 3"    output="F" context="TestCtx2" allow_error="F" processor="highlight"
            id="test_id1"'''))

        self.assertEqual(None, snippet.pattern().language(''' langaa="Python 3"    output="F" context="TestCtx2" allow_error="F" processor="highlight"
            id="test_id1"'''))

        self.assertEqual(None, snippet.pattern().language('''  output="F" context="TestCtx2" allow_error="F" processor="highlight"
            id="test_id1"'''))

    def test_echo1(self):
        snippet = Snippet(TestSnippetPattern.DATA1)
        self.fail()

    def test_echo2(self):
        snippet = Snippet(TestSnippetPattern.DATA2)

        self.assertEqual(None, snippet.pattern().echo(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" processor="highlight"
             id="test_id1"'''))

        self.assertTrue(snippet.pattern().echo(''' lang="Python 3"    output="F" context="TestCtx2" echo="T" allow_error="F" processor="highlight"
             id="test_id1"'''))

        self.assertEqual(None, snippet.pattern().echo(''' lang="Python 3"    output="F" aecho="1" echoqq="False" context="TestCtx2" allow_error="F" processor="highlight"
            id="test_id1"'''))

        self.assertTrue(snippet.pattern().echo('echo="T"'))
        self.assertTrue(snippet.pattern().echo('echo="1"'))
        self.assertTrue(snippet.pattern().echo('echo="True"'))
        self.assertTrue(snippet.pattern().echo('echo="Y"'))
        self.assertTrue(snippet.pattern().echo('echo="t"'))
        self.assertTrue(snippet.pattern().echo('echo="y"'))
        self.assertTrue(snippet.pattern().echo('echo="YES"'))
        self.assertTrue(snippet.pattern().echo('echo="yes"'))

        self.assertFalse(snippet.pattern().echo('echo="F"'))
        self.assertFalse(snippet.pattern().echo('echo="False"'))
        self.assertFalse(snippet.pattern().echo('echo="0"'))
        self.assertFalse(snippet.pattern().echo('echo="N"'))
        self.assertFalse(snippet.pattern().echo(' echo="No"'))
        self.assertFalse(snippet.pattern().echo('echo="no" '))

        with self.assertRaises(InvalidBoolValueError):
            snippet.pattern().echo('echo="X"')

    def test_output1(self):
        snippet = Snippet(TestSnippetPattern.DATA1)
        self.fail()

    def test_output2(self):
        snippet = Snippet(TestSnippetPattern.DATA2)

        self.assertEqual(None, snippet.pattern().output(''' lang="Python 3"  context="TestCtx2" allow_error="F" processor="highlight"
                     id="test_id1"'''))

        self.assertFalse(snippet.pattern().output(''' lang="Python 3"output="F" context="TestCtx2" echo="T" allow_error="F" processor="highlight"
                     id="test_id1"'''))

        self.assertEqual(None, snippet.pattern().output(''' lang="Python 3"   qqoutput="F" outputww="0" context="TestCtx2" allow_error="F" processor="highlight"
                    id="test_id1"'''))

        self.assertTrue(snippet.pattern().output('output="T"'))
        self.assertTrue(snippet.pattern().output('output="1"'))
        self.assertTrue(snippet.pattern().output('output="True"'))
        self.assertTrue(snippet.pattern().output('output="Y"'))
        self.assertTrue(snippet.pattern().output('output="t"'))
        self.assertTrue(snippet.pattern().output('output="y"'))
        self.assertTrue(snippet.pattern().output('output="YES"'))
        self.assertTrue(snippet.pattern().output('output="yes"'))

        self.assertFalse(snippet.pattern().output('output="F"'))
        self.assertFalse(snippet.pattern().output('output=" False "'))
        self.assertFalse(snippet.pattern().output('output="0"'))
        self.assertFalse(snippet.pattern().output('output="N"'))
        self.assertFalse(snippet.pattern().output(' output="No"'))
        self.assertFalse(snippet.pattern().output('output="no" '))

        with self.assertRaises(InvalidBoolValueError):
            snippet.pattern().output('output="X"')

    def test_context1(self):
        snippet = Snippet(TestSnippetPattern.DATA1)
        self.fail()

    def test_context2(self):
        snippet = Snippet(TestSnippetPattern.DATA2)

        self.assertEqual('TestCtx2', snippet.pattern().context(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" processor="highlight"
             id="test_id1"'''))

        self.assertEqual(None, snippet.pattern().context(''' lang="Python 3"    output="F" qqcontext="TestCtx2" allow_error="F" processor="highlight"
            id="test_id1"'''))

        self.assertEqual(None, snippet.pattern().context(''' lang="Python 3"    output="F" contextqq="TestCtx2" allow_error="F" processor="highlight"
            id="test_id1"'''))

        self.assertEqual(None, snippet.pattern().context('''  output="F"  allow_error="F" processor="highlight"
            id="test_id1"'''))

    def test_id1(self):
        snippet = Snippet(TestSnippetPattern.DATA1)
        self.fail()

    def test_id2(self):
        snippet = Snippet(TestSnippetPattern.DATA2)

        self.assertEqual('test_id1', snippet.pattern().id(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" processor="highlight"
             id="test_id1"'''))

        self.assertEqual(None, snippet.pattern().id(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" processor="highlight"
            aid="test_id1"'''))

        self.assertEqual(None, snippet.pattern().id(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" processor="highlight"
            idw="test_id1"'''))

        self.assertEqual(None, snippet.pattern().id('''  output="F" context="TestCtx2" allow_error="F" processor="highlight"  '''))

    def test_timeout1(self):
        snippet = Snippet(TestSnippetPattern.DATA1)
        self.fail()

    def test_timeout2(self):
        snippet = Snippet(TestSnippetPattern.DATA2)

        self.assertEqual(2.5, snippet.pattern().timeout(''' lang="Python 3"    output="F" context="TestCtx2" timeout="2500" allow_error="F" processor="highlight"
             id="test_id1"'''))

        self.assertEqual(None, snippet.pattern().timeout(''' lang="Python 3"  aatimeout="2500"   output="F" context="TestCtx2" allow_error="F" processor="highlight"
            aid="test_id1"'''))

        self.assertEqual(None, snippet.pattern().timeout(''' lang="Python 3"  timeoutaa="2500"  output="F" context="TestCtx2" allow_error="F" processor="highlight"
            idw="test_id1"'''))

        self.assertEqual(None, snippet.pattern().timeout('''  output="F" context="TestCtx2" allow_error="F" processor="highlight"  '''))

        with self.assertRaises(TimeoutValueError):
            snippet.pattern().timeout(''' lang="Python 3"  timeout="invalid"  output="F" context="TestCtx2" allow_error="F" processor="highlight"
            idw="test_id1"''')

    def test_error1(self):
        snippet = Snippet(TestSnippetPattern.DATA1)
        self.fail()

    def test_error2(self):
        snippet = Snippet(TestSnippetPattern.DATA2)

        self.assertEqual(None, snippet.pattern().error(''' lang="Python 3"    output="F" context="TestCtx2"  processor="highlight"
                     id="test_id1"'''))

        self.assertTrue(snippet.pattern().error(''' lang="Python 3"    output="F" context="TestCtx2" echo="T" allow_error="1" processor="highlight"
                     id="test_id1"'''))

        self.assertEqual(None, snippet.pattern().error(''' lang="Python 3"    output="F" aecho="1" echoqq="False" context="TestCtx2" aallow_error="F" allow_errorq="1" processor="highlight"
                    id="test_id1"'''))

        self.assertTrue(snippet.pattern().error('allow_error="T"'))
        self.assertTrue(snippet.pattern().error('allow_error="1"'))
        self.assertTrue(snippet.pattern().error('allow_error="True"'))
        self.assertTrue(snippet.pattern().error('allow_error="Y"'))
        self.assertTrue(snippet.pattern().error('allow_error="t"'))
        self.assertTrue(snippet.pattern().error('allow_error="y"'))
        self.assertTrue(snippet.pattern().error('allow_error="YES"'))
        self.assertTrue(snippet.pattern().error('allow_error="yes"'))

        self.assertFalse(snippet.pattern().error('allow_error="F"'))
        self.assertFalse(snippet.pattern().error('allow_error="False"'))
        self.assertFalse(snippet.pattern().error('allow_error="0"'))
        self.assertFalse(snippet.pattern().error('allow_error="N"'))
        self.assertFalse(snippet.pattern().error(' allow_error="No"'))
        self.assertFalse(snippet.pattern().error('allow_error="no" '))

        with self.assertRaises(InvalidBoolValueError):
            snippet.pattern().error('allow_error="X"')

    def test_output_type1(self):
        snippet = Snippet(TestSnippetPattern.DATA1)
        self.fail()

    def test_output_type2(self):
        snippet = Snippet(TestSnippetPattern.DATA2)

        self.assertTrue(snippet.pattern().output_type(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" output_type="Stdout, Image" processor="highlight"
             id="test_id1"''').is_enabled('Stdout'))

        self.assertTrue(snippet.pattern().output_type(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" output_type="Stdout, Image" processor="highlight"
             id="test_id1"''').is_enabled('Image'))

        self.assertFalse(snippet.pattern().output_type(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" output_type="Stdout, Image" processor="highlight"
             id="test_id1"''').is_enabled('Stderr'))

        self.assertFalse(snippet.pattern().output_type(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" output_type="Stdout, Image" processor="highlight"
             id="test_id1"''').is_enabled('Text'))

        self.assertTrue(snippet.pattern().output_type(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" processor="highlight"
             id="test_id1"''').is_enabled('Stdout'))

        self.assertTrue(snippet.pattern().output_type(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" processor="highlight"
             id="test_id1"''').is_enabled('Image'))

    def test_processor1(self):
        snippet = Snippet(TestSnippetPattern.DATA1)
        self.fail()

    def test_processor2(self):
        snippet = Snippet(TestSnippetPattern.DATA2)

        self.assertEqual('highlight', snippet.pattern().processor(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" processor="highlight"
             id="test_id1"'''))

        self.assertEqual(None, snippet.pattern().processor(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" qddprocessor="highlight"
            id="test_id1"'''))

        self.assertEqual(None, snippet.pattern().processor(''' lang="Python 3"    output="F" context="TestCtx2" allow_error="F" processorqq="highlight"
            id="test_id1"'''))

        self.assertEqual(None, snippet.pattern().processor('''  output="F" context="TestCtx2" allow_error="F"
            id="test_id1"'''))

    def test_echo_lines1(self):
        snippet = Snippet(TestSnippetPattern.DATA1)
        self.fail()

    def test_echo_lines2(self):
        snippet = Snippet(TestSnippetPattern.DATA2)

        lines = snippet.pattern().echo_lines('echo_lines="5,6, 10"')
        self.assertEqual(2, len(lines))
        self.assertFalse(lines[0])
        self.assertEqual(3, len(lines[1]))
        self.assertEqual(6, lines[1][1])

        lines = snippet.pattern().echo_lines('echo_lines="1, 5-15, 23"')
        self.assertEqual(2, len(lines))
        self.assertFalse(lines[0])
        self.assertEqual(13, len(lines[1]))
        self.assertEqual(7, lines[1][3])

        lines = snippet.pattern().echo_lines('echo_lines="! 1, 5 - 15, 23"')
        self.assertEqual(2, len(lines))
        self.assertTrue(lines[0])
        self.assertEqual(13, len(lines[1]))
        self.assertEqual(7, lines[1][3])

        with self.assertRaises(ValueError):
            lines = snippet.pattern().echo_lines('echo_lines="! 1, 5 - 15, 23 aqqw"')
