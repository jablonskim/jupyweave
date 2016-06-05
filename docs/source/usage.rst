Jupyweave usage
===============

Processing documents
--------------------

Documents can be processed with Jupyweave by providing their file names as arguments to Jupyweave:

    ::

        jupyweave example.html example.tex example1.md example2.md

All provided files will be parsed, code snippets found in documents will be executed and results will be pasted into
final documents, according to :doc:`configuration file <config>`, code :ref:`snippets settings <creating-docs>` and
:doc:`processors <processors>`.

`Markup language <https://en.wikipedia.org/wiki/Markup_language>`_ used in document is recognized by
document's extension. For more information see :ref:`extensions`.


.. _creating-docs:

Creating documents
------------------

Documents for Jupyweave can be created by modifying markup documents (eg. HTML, LaTeX, Markdown).
Source code in some programming or scripting language can by pasted into this documents. The code is then executed
during documents processing and its results are pasted into final document, according to selected
:doc:`configuration file <config>`, used :doc:`processors <processors>` and source code snippet settings.
The code snippets are processed by `Jupyter <http://jupyter.org/>`_.

Basic tags
~~~~~~~~~~

    * ``begin``, ``end``
        Source code must be included between ``begin`` and ``end`` tags. This tags are looked for during processing,
        source code is extracted, executed, and results are processed using :doc:`processor <processors>`.
        The ``begin`` tag has to contain :ref:`settings-tag` which are extracted and processed too.

    * ``output``
        This tag is repleced by results of one of previously executed code snippets. It must contain an ``id``
        (inside it's ``settings``) of code snippet, which result has to be pasted into document.
        The code snippet with this ``id`` has to be defined in the document before it is used by ``output``.

    * ``default_settings``
        Defines default :ref:`settings <settings-tag>` for all code snippets in current document.
        It may be used once per document and can be defined anywhere inside this document.
        It's content is parsed before any ``begin``, ``end`` or ``output`` tag.
        During processint it is parsed and then removed from final document.
        Every setting defined by this tag is used if there are no such setting defined in ``begin`` tag.

All tags may be speciffic to selected configuration file and document's markup language.
For default tags see :ref:`def-config-files`.


.. _settings-tag:

Settings
~~~~~~~~

There are many setting tags that can be defined in ``begin`` and ``default_settings``:

    * ``language``
        Defines sippet's programming language. Used by `Jupyter <http://jupyter.org/>`_.
        There is no default language provided by implementation, so ``language`` in ``default_settings``
        or in ``begin`` must be defined.

    * ``echo``
        Boolean value indicating if the source code will be pasted into the final document. Default value: **True**.

    * ``output``
        Boolean value indicating if the results of execution will be pasted into the final document.
        Default value: **True**.

    * ``context``
        A string defining the *context of execution*. Snippets exetuted in the same context can see variable and
        environment modifications caused by previous snippets executed in this context. If no ``context`` is provided,
        default context is used. Contexts are different for each programming language and each document.

    * ``timeout``
        Contains time in milliseconds, which defines how long the code snippet can be executed.
        Execution is terminated after this time. It overrides timeouts defined in :ref:`execution-timeouts` in
        configuration file.

    * ``error``
        Boolean value. **True** indicates that errors are allowed, and error or exception during execution of
        that snippet terminates execution of that snippet only. Error message will be pasted into results.
        **False** indicates that errors during execution will terminate processing of the whole document.
        Error message will be printed on screen.

    * ``output_type``
        Comma or space separated strings representing which results will be pasted into final documents.
        Avaliable options:

            * ``Stdout`` - Standard output
            * ``Stderr`` - Standard error output
            * ``Text`` - Text other than stderr and stdout. Implementation defined.
            * ``Image`` - Images
            * ``PDF`` - PDF files
            * ``All`` - All output types. Overrides other values.

        The types of results depends on implementation of Jupyter kernels for different languages. Case is ignored.

    * ``processor``
        String defining :doc:`user processor <processors>` used for snippet execution and results processing.
        Default processor for markup language is used if ``processor`` not provided.

    * ``echo_lines``
        Defines numbers of lines of source code that can be pasted into result. It supports comma separated values,
        where each value may be a **number** or a **range** (two numbers separated by ``:`` or ``-``).
        There can be also a ``!`` character at the begining of the ``echo_lines`` string. In that case, all lines
        except defined are pasted into the result. For example ``!1,4-6`` means all lines except 1, 4, 5, 6
        will be displayed. Lines are numbered from 1.

    * ``image_name``
        Defines the file name, which will be used to save image generated by execution of the code snippet.
        The name is used for the whole snippet, so if there will be more than one image generated, the last image
        overwrites all previous images.

    * ``image_width``
        An integer defining generated image width.

    * ``image_height``
        An integer defining generated image height.

    * ``image_align``
        Image alignment in final document. It can be ``Left``, ``Right`` or ``Center``. Case is ignored.
        If not provided default value for markup language is used.


There is also ``snippet_id`` setting. It can be defined in ``begin`` and ``output`` tag's settings. If it is defined
in ``begin``, the results of code snippet executions are saved with this ID. Then, if there is ane ``output`` tag
with this ``snippet_id``, the saved results is pasted into final document. The ``snippet_id`` must be used before in
any ``begin`` tag.

All boolean values used in settings may be ``t``, ``true``, ``y``, ``yes`` or ``1`` for **True** and
``n``, ``no``, ``f``, ``false`` or ``0`` for **False**. Case is ignored.

All tags may be speciffic to selected configuration file and document's markup language.
For default tags see :ref:`def-config-files`.


.. _processing-results:

Processing results
~~~~~~~~~~~~~~~~~~

TODO: processors


Changing configuration
----------------------

To process documents using other configuration add ``--config=config_file.json`` option to command line.
``config_file.json`` must be valid :doc:`Jupyweave Configuration <config>` file.
With this option, all documents will be parsed and processed using provided configuration.

For more information about configuration files see :doc:`config` section.
