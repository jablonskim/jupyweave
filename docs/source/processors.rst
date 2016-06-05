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

TODO


.. _default-processors:

Default processors
------------------

TODO: html, markdown, latex


.. _user-processors:

User processors
---------------

TODO
