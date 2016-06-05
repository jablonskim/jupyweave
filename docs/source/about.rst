About Jupyweave
===============

Jupyweave is a dynamic report generation framework. The reports can be written in
`markup languages <https://en.wikipedia.org/wiki/Markup_language>`_, and may
contain dynamic parts written with some programming or scripting language. The reports can be any kind of documents,
books or articles. During processing this reports with Jupyweave the dynamic parts are evaluated and its results
are pasted into final, static documents. Base implementation of Jupyweave supports
`HTML <https://www.w3.org/html/>`_, `LaTeX <https://www.latex-project.org/>`_ and
`Markdown <http://daringfireball.net/projects/markdown/>`_ documents.
More markup languages may be easily defined by the user.

The dynamic code fragments are evaluated by `Jupyter <http://jupyter.org/>`_, so they can be written in any language
supported by `Jupyter kernels <https://github.com/ipython/ipython/wiki/IPython-kernels-for-other-languages>`_.
The behaviour of processing documents by Jupyweave can be easily
controlled by :doc:`configuration files <config>` and :doc:`user defined processors <processors>`.

Jupyweave is base on the idea of `Literate programming <https://en.wikipedia.org/wiki/Literate_programming>`_.

Source code of Jupyweave can be found on `Github <https://github.com/jablonskim/jupyweave>`_.
Package can be downloaded from `PyPI <https://pypi.python.org/pypi/jupyweave>`_.
