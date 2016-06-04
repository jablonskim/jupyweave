Installation
============

Installing Jupyweave package
----------------------------

To install Jupyweave from PyPI just run:

    ::

        pip install jupyweave

All required dependencies should be installed automatically.
Be sure to run this command with pip for Python 3. Jupyweave is not working with Python 2 at this time.

Installing configuration files and documents processors
-------------------------------------------------------

After installing Jupyweave run the following command:

    ::

        jupyweave_install

It will create ``jupyweave/config/``, ``jupyweave/processors/`` directories and create
:doc:`configuration files <config>` and :doc:`processors <processors>` in them.
This directories will be created in one of the following locations:

    * ``/usr/local/share`` - when running on Linux systems with root privilages,
    * ``$HOME/.local/share`` - when running on Linux systems without root privilages,
    * ``%PROGRAMDATA%`` - when running on Windows systems with Administrator rights,
    * ``%APPDATA%`` - when running on Windows systems without Administrator rights

For more details about Jupyweave directories see :doc:`config` or :doc:`processors`.
