Document processing
===================

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

TODO: html, markdown, latex


.. _user-processors:

User processors
---------------

TODO
