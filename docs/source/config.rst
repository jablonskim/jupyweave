Configuration
=============


About Jupyweave configuration
-----------------------------

Jupyweave is configured by single configuration file.
This configuration is used to parse all documents processed in single run.
It can be provided by user or Jupyweave can use default configuration provided in package.
For more information see :ref:`using-config-files`, :ref:`config-file-structure` or :ref:`def-config-files`.


.. _using-config-files:

Using configuration files
-------------------------

To process documents using other configuration add ``--config=config_file.json`` option to command line.
With this option, all processed documents will be parsed and processed using provided configuration.
Without this option, all processed documents will be parsed using default configuration ``defconfig.json``
located in Jupyweave config directory.

Jupyweave configuration directories (``jupyweave/config/``) are in the following locations:

    * ``/usr/local/share`` - system directory on Linux,
    * ``$HOME/.local/share`` - user directory on Linux,
    * ``%PROGRAMDATA%`` - system directory on Windows,
    * ``%APPDATA%`` - user directory on Windows.

The file provided to ``--config`` option is searched in the following order:

    * absolute or relative (to the current working directory) file path,
    * file in user directory,
    * file in system directory,

The first found file is used as a configuration file.
Error message is displayed if no configuration file with provided file name was found.

New configuration files can be created by copying default configuration file to system directory,
user directory or some other directory and modifying this file.


.. _config-file-structure:

Configuration files structure
-----------------------------

Configuration file is written in `JSON <http://www.json.org/>`_. It has to contain following sections:

    * :ref:`markup_languages <markup-languages>`
    * :ref:`extensions <extensions>`
    * :ref:`output <output>`
    * :ref:`execution_timeouts <execution-timeouts>`
    * :ref:`code_snippets <code-snippets>`


.. _markup-languages:

Markup languages
~~~~~~~~~~~~~~~~

Contains an array of strings representing `markup languages <https://en.wikipedia.org/wiki/Markup_language>`_ names.
All languages defined in this array are recognized by Jupyweave and can be processed.


.. _extensions:

Extensions
~~~~~~~~~~

Contains dictionary of string to array mappings. The string is :ref:`markup language name <markup-languages>`
and the array contains strings with file extensions of markup language files. Extensions are provided without dot.

This setting is used for automatic recognition of markup language of document.


.. _output:

Output
~~~~~~

Contains information about saving results of document procecssing.
It consists of the following sections:

    * ``results_base`` - defines relative or absolute base directory for results.
    * ``filename`` - defines result's file name. May contain patterns defined in ``patterns`` option. Result of document processing wil be saved to file with this name, inside ``results_base`` directory.
    * ``data_dir`` - defines base directory for additional data (images etc.). This directory will be created in ``results_base`` directory and all additional files will be saved inside it.
    * ``patterns`` - defines patterns that can be used in ``filename``, ``results_base`` and ``data_dir``. This patterns are replaced with proper content during execution. There are following patterns:

        * ``name`` - for filename of input file
        * ``extension`` - extension of input file (without dot)


.. _execution-timeouts:

Execution timeouts
~~~~~~~~~~~~~~~~~~

Contains time in milliseconds, which defines how long every code snippet can be executed.
Execution is terminated after this time. It consists of the following options:

    * ``languages`` - mappings of programming languages to times. Used to define timeout separately for each language used in snippets.
    * ``default`` - time used for languages not defines in ``languages`` section.


.. _code-snippets:

Code snippets
~~~~~~~~~~~~~

Defines patterns used in documents. May contain definition for each defined markup language and ``default`` definition.
Each definition consists of the following options:

    * ``begin``
    * ``end``
    * ``output``
    * ``default_settings``
    * ``settings``
    * ``patterns``

For information about ``begin``, ``end``, ``output`` and ``default_settings`` see :ref:`creating-docs`.

The ``settings`` option consists of:

    * ``language``
    * ``echo``
    * ``output``
    * ``context``
    * ``snippet_id``
    * ``timeout``
    * ``error``
    * ``output_type``
    * ``processor``
    * ``echo_lines``
    * ``image_name``
    * ``image_width``
    * ``image_height``
    * ``image_align``

All settings are described in :ref:`creating-docs` section.

The ``patterns`` option contains patterns that can be used in all other patterns and are replaced with proper content
during execution. It consists of:

    * ``settings`` - it may be used in ``begin``, ``output`` and ``default_settings`` for defining patterns for settings.
    * ``language``
    * ``echo``
    * ``output``
    * ``context``
    * ``snippet_id``
    * ``timeout``
    * ``error``
    * ``output_type``
    * ``processor``
    * ``echo_lines``
    * ``image_name``
    * ``image_width``
    * ``image_height``
    * ``image_align``

All patterns except ``settings`` are used in corresponding ``settings`` option.

For more information, see :ref:`creating-docs`.


.. _def-config-files:

Default configuration files
---------------------------

There are two default configuration files provided within the Jupyweave package:


.. _defconfig-json:

`defconfig.json <https://github.com/jablonskim/jupyweave/blob/master/jupyweave/configs/defconfig.json>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Default configuration. Defines `HTML <https://www.w3.org/html/>`_,
`Markdown <http://daringfireball.net/projects/markdown/>`_ and
`LaTeX <https://www.latex-project.org/>`_ markup languages.
Available document's extensions are ``html`` and ``htm`` for HTML, ``md``, ``markdown``, ``mdown``, ``mkdn``, ``mkd``
for Markdown and ``tex`` for LaTeX.

The results will be saved to ``jupyweave_outputs/`` directory, with filename ``{NAME}.{EXT}``. Images will be saved to
``{NAME}_{EXT}_data`` directory. ``{NAME}`` and ``{EXT}`` will be replaced with name and extension of the input file.

Default execution timeout is 1000ms. Execution timeout for Python 3 is 2000ms.


The ``code_snippets`` options for `HTML <https://www.w3.org/html/>`_ are defined as follows:

    * ``<snippet{S}>`` - **begin** tag, ``{S}`` is pattern for extracting snippet settings,
    * ``</snippet>`` - **end** tag
    * ``<output{S}>`` - **output** tag, ``{S}`` is pattern for extracting output settings,
    * ``<default_settings{S}>`` - **default_settings** tag, ``{S}`` is pattern for extracting default settings.

All ``settings`` are defined in form ``setting_name="{X}"`` where ``{X}`` is speciffic for each setting and is used to
extract setting during execution.


The ``code_snippets`` options for `LaTeX <https://www.latex-project.org/>`_ are defined as follows:

    * ``\begin_code{@S}`` - **begin** tag, ``@S`` is pattern for extracting snippet settings,
    * ``\end_code`` - **end** tag
    * ``\snippet_output{@S}`` - **output** tag, ``@S`` is pattern for extracting output settings,
    * ``\default_settings{@S}`` - **default_settings** tag, ``@S`` is pattern for extracting default settings.

All ``settings`` are defined in form ``setting_name[@X]`` where ``@X`` is speciffic for each setting and is used to
extract setting during execution.


The ``code_snippets`` options for other markup languages are defined as follows:

    * ``<#{S}>`` - **begin** tag, ``{S}`` is pattern for extracting snippet settings,
    * ``<@>`` - **end** tag
    * ``<${S}>`` - **output** tag, ``{S}`` is pattern for extracting output settings,
    * ``<!!!{S}>`` - **default_settings** tag, ``{S}`` is pattern for extracting default settings.

All ``settings`` (except ``language``) are defined in form ``setting_name={X}`` where ``{X}`` is speciffic for each setting and is used to
extract setting during execution. The ``language`` setting is defined as ``[{L}]``.


.. _knitr-config-json:

`knitr_config.json <https://github.com/jablonskim/jupyweave/blob/master/jupyweave/configs/knitr_config.json>`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alternative default configuration. Can be used by providing ``--config=knitr_config.json`` argument to Jupyweave.
It is proof of concept configuration, that tries to define similar syntax for that one used
in `Knitr <http://yihui.name/knitr/>`_.

All settings except ``code_snippets`` are the same as for :ref:`defconfig-json`.


The ``code_snippets`` options for `HTML <https://www.w3.org/html/>`_ are defined as follows:

    * ``<!--begin.code{S}\n`` - **begin** tag, ``{S}`` is pattern for extracting snippet settings,
    * ``end.code-->`` - **end** tag
    * ``<!--output.result{S}-->`` - **output** tag, ``{S}`` is pattern for extracting output settings,
    * ``<!--default.settings{S}-->`` - **default_settings** tag, ``{S}`` is pattern for extracting default settings.

All ``settings`` are defined in form ``setting_name={X}`` where ``{X}`` is speciffic for each setting and is used to
extract setting during execution.


The ``code_snippets`` options for `LaTeX <https://www.latex-project.org/>`_ are defined as follows:

    * ``<<@S>>=`` - **begin** tag, ``@S`` is pattern for extracting snippet settings,
    * ``@\n`` - **end** tag
    * ``\output{@S}`` - **output** tag, ``@S`` is pattern for extracting output settings,
    * ``\defsettings{@S}`` - **default_settings** tag, ``@S`` is pattern for extracting default settings.

All ``settings`` are defined in form ``setting_name=@X`` where ``@X`` is speciffic for each setting and is used to
extract setting during execution. The ``language`` setting is defined as ``[@L]``.


The ``code_snippets`` options for `Markdown <http://daringfireball.net/projects/markdown/>`_ are defined as follows:

    * `````{{S}}`` - **begin** tag, ``{S}`` is pattern for extracting snippet settings,
    * ``````` - **end** tag
    * ``[Out]:#({S})`` - **output** tag, ``{S}`` is pattern for extracting output settings,
    * ``[Def]:#({S})`` - **default_settings** tag, ``{S}`` is pattern for extracting default settings.

All ``settings`` (except ``language``) are defined in form ``setting_name={X}`` where ``{X}`` is speciffic for each setting and is used to
extract setting during execution. The ``language`` setting is defined as ``[{L}]``.
