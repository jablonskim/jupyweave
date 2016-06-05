Document processing
===================


.. _about-processing:

About processing
----------------

Processors are simple files written in Python used for processing results of snippets. They allow to modify various
aspects of saving results to final documents. For all capabilities of processors see :ref:`structure-of-processors`.

Processors are based on Python classes. There is a :ref:`base Processor <structure-of-processors>`,
:ref:`markup language processors <default-processors>` (inherited from base),
and :ref:`user defined processors <user-processors>` (inherited from one of merkup language processors
or other user processors).

Processors are used in the following order:

    * If there is ``processor`` setting in ``settings`` of tag, this processor name is concatenated (using underscore)
      with name of the markup language and the word *processor*. File with extension ``.py`` and this name is searched
      for in directories defined below. If the file is not found or has invalid format, processing is terminated.
      Otherwise it is used for processing. (For example: if ``processor`` setting value was ``user_test`` and
      the used markup language is HTML, the name of the file will be ``user_test_html_processor.py``)

    * If there is no ``processor`` setting, file with the name ``markup_processor.py`` (with used markup language name)
      is searched for in directories defined below and used for processing.

    * If it is not found, the file with name ``processor.py`` (base processor) is used for processing.


Processors are located in the following directories:

    * ``/usr/local/share/jupyweave/processors`` - system directory on Linux,
    * ``$HOME/.local/share/jupyweave/processors`` - user directory on Linux,
    * ``%PROGRAMDATA%/jupyweave/processors`` - system directory on Windows,
    * ``%APPDATA%/jupyweave/processors`` - user directory on Windows.
    * Jupyweave package location

They are searched for in the following order:

    * User directory
    * System directory
    * Package location

For defining own processors, see :ref:`user-processors`.


.. _structure-of-processors:

Structure of processors
-----------------------

Processors are Python files with single class named ``Processor`` defined inside it. This class can be inherited from
other processors.

Base processor class contains following methods and fields:

    * ``execute``
        Method with one parameter. The parameter is code for execution in context of currently executed code snippet.
        It can be used from other methods for executing arbitrary code. It returns results of execution.

    * ``save_to_file``
        Method with two parameters. The first of them is data to be saved to file, second, the file's extension.
        It saves data to file with generated name with provided extension and returns relative path to that file.
        The path may be used in finel document.

    * ``begin``
        Method with no arguments. It is callec by implementation before execution of every snippet. It allows to
        execute user-defined code before snippets. It should return results of execution, which will be pasted into
        final document. Default implementation of this method in base class is empty and returns empty string.

    * ``end``
        Method with no arguments. It is callec by implementation after execution of every snippet. It allows to
        execute user-defined code after snippets. It should return results of execution, which will be pasted into
        final document. Default implementation of this method in base class is empty and returns empty string.

    * ``source``
        Method with one argument - the source code. It processes source code before pasting into final document.
        It can be used for highlighting, line numbering etc. It is called by implementation and returns
        processed code.

    * ``text``
        Method with single text argument. It may be called multiple times durign processing single snippet with
        partial results as its argument. It may be used for escaping, reformatting etc. Returns processed text.

    * ``image``
        Method with two arguments. First of them is image data, second, the
        `mime type <https://en.wikipedia.org/wiki/Media_type>`_ of that data. It is used for
        saving images. Base implementation returns path to the saved image.

    * ``result``
        Method with single argument. The argument is result of whole execution. It may be used for formatting
        results. It contains processed image data (paths). It returns processed results.

    * ``language``
        Field that contains language name used in code snippet.

    * ``settings``
        Contains settings string form ``settings`` field from ``begin`` snippet tag.

    * ``image_width``
        Contains integer that can be used as image width or *None* if no width was defined in ``settings`` tag.

    * ``image_height``
        Contains integer that can be used as image height or *None* if no height was defined in ``settings`` tag.

    * ``image_align``
        Contains image align type that can be used to format image or *None* if not specified.


Every method may be overriden in derived processor. If there is no overrided method, the one from base class will be
called. This allows to define :ref:`user processors <user-processors>` for speciffic operations on
selected types of results.

Default implementation of base processor can be found
`here <https://github.com/jablonskim/jupyweave/blob/master/jupyweave/processors/processor.py>`_


.. _default-processors:

Default processors
------------------

There are one default processor for each defined `markup language <https://en.wikipedia.org/wiki/Markup_language>`_.
They are inherited from :ref:`base processor <structure-of-processors>`.


`html_processor.py <https://github.com/jablonskim/jupyweave/blob/master/jupyweave/processors/html_processor.py>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used for processing HTML documents. It redefines the following methods:

    * ``source``
        Puts the source code into raw code tag.

    * ``result``
        Puts the result of snippet execution into html paragraph tag.

    * ``text``
        It escapes all html tags, so that all tags will be displayed in final document (and not intepreted as tags).
        It also replaces new lines with new line tags.

    * ``image``
        Uses image method from base class to save image and get its path, then puts this path into html image tag
        and adds some styles according to image formatting settings provided in ``settings`` tag.


`latex_processor.py <https://github.com/jablonskim/jupyweave/blob/master/jupyweave/processors/latex_processor.py>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used for processing LaTeX documents. It redefines the following methods:

    * ``source``
        Returns the code inside raw code section.

    * ``text``
        Escapes LaTeX instructions and adds new lines.

    * ``image``
        Uses image method from base class to save image and get its path, then using it creates image section.
        It also uses image formatting settings from ``settings`` tag and parses user defined settings ``img_caption``
        and ``img_label`` that **allows to define caption and label** of the image.


`markdown_processor.py <https://github.com/jablonskim/jupyweave/blob/master/jupyweave/processors/markdown_processor.py>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used for processing HTML documents. It redefines the following methods:

    * ``source``
        Puts source code into code section.

    * ``result``
        Adds some new lines.

    * ``text``
        Adds new lines.

    * ``image``
        Uses image method from base class to save image and get its path, then using it pastes image into document.


.. _user-processors:

User processors
---------------

User processors are defined by creating a Python file with class ``Processor``. The file must be in
:ref:`system directory or user directory <about-processing>`. The file has to be inherited from one of
:ref:`markup processors <default-processors>`. The proposed solution is to use import like:

    ::

        from latex_processor import Processor as BaseProcessor

This import will work if used only by Jupyweave core.
User processor then will be derived from ``BaseProcessor``. It may overload one or more methods from ``BaseProcessor``
class.

There are some user defined processors provided with the package to simplify usage of Jupyweave:

    * `highlight_html_processor.py <https://github.com/jablonskim/jupyweave/blob/master/jupyweave/user_processors/highlight_html_processor.py>`_
        Highlights source code pasted into HTML documents.

    * `no_escape_html_processor.py <https://github.com/jablonskim/jupyweave/blob/master/jupyweave/user_processors/no_escape_html_processor.py>`_
        Allows to dynamically generate HTML document by removing escaping of results.

    * `no_escape_latex_processor.py <https://github.com/jablonskim/jupyweave/blob/master/jupyweave/user_processors/no_escape_latex_processor.py>`_
        Allows to dynamically generate LaTeX document by removing escaping of results.

    * `no_escape_markdown_processor.py <https://github.com/jablonskim/jupyweave/blob/master/jupyweave/user_processors/no_escape_markdown_processor.py>`_
        Allows to dynamically generate Markdown document by removing escaping of results.

    * `python_latex_processor.py <https://github.com/jablonskim/jupyweave/blob/master/jupyweave/user_processors/python_latex_processor.py>`_
        Defines LaTeX processor speciffic for Python snippets. It allows to save images to PDF files instead of PNG.

    * `r_latex_processor.py <https://github.com/jablonskim/jupyweave/blob/master/jupyweave/user_processors/r_latex_processor.py>`_
        Defines LaTeX processor speciffic for R snippets. It allows to save images to PDF files instead of PNG.

    * `sql_html_processor.py <https://github.com/jablonskim/jupyweave/blob/master/jupyweave/user_processors/sql_html_processor.py>`_
        It allows to use proof-of-concept SQL Jupyter kernel with HTML.

    * `sql_latex_processor.py <https://github.com/jablonskim/jupyweave/blob/master/jupyweave/user_processors/sql_latex_processor.py>`_
        It allows to use proof-of-concept SQL Jupyter kernel with LaTeX.
