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

TODO: snippets, settings, processors


Changing configuration
----------------------

To process documents using other configuration add ``--config=config_file.json`` option to command line.
``config_file.json`` must be valid :doc:`Jupyweave Configuration <config>` file.
With this option, all documents will be parsed and processed using provided configuration.

For more information about configuration files see :doc:`config` section.
