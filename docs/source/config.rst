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

TODO


.. _def-config-files:

Default configuration files
---------------------------

TODO
