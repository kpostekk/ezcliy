Command
===========
.. py:currentmodule:: ezcliy.commands

.. autoclass:: Command
    :members:
    :member-order: bysource

Subcommands
------------

Ez cliy allows to create subcommands.

.. literalinclude:: _static/creating_subcommands.py

Help
-----

Ez cliy has built-in help generator. It can be invoked by typing ``--help``. Also it will executed when command has no arguments or values.

.. tip::

    You can change that behaviour by setting :attr:`ezcliy.Command.allow_empty_calls` on ``True``

