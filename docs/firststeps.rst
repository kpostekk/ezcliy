First steps
============

Create command
---------------

Let's create simple command.

.. code-block:: python

    from ezcliy import Command


    class SmallTextProcessor(Command):
        def invoke(self):
            print(f'You have passed {len(self.values)} arguments!')


    if __name__ == '__main__':
        SmallTextProcessor().cli_entry()

All cleaned values are in ``self.values``.

That will count passed values.

.. code-block::

    python3 main.py first second
    You have passed 2 arguments!

Add parameters
---------------

Now we will add flag (``-v``) and keyval (``--verbose-level=debug``)

.. code-block:: python

    from ezcliy import Command, Flag, KeyVal


    class SmallTextProcessor(Command):
        verbose = Flag('-v', '--verbose')
        verbosity_level = KeyVal('--verbose-level', default='info')

        def invoke(self):
            if self.verbose:
                print(f'Logging enabled, {self.verbosity_level.value=}')
            print(f'You have passed {len(self.values)} arguments!')


    if __name__ == '__main__':
        SmallTextProcessor().cli_entry()

Flags are boolean values, we can put them directly into ``if``s

.. code-block::

    python3 main.py first second -v --verbose-level=debug
    Logging enabled, self.verbosity_level.value='debug'
    You have passed 2 arguments!

Add positionals
----------------

Positionals are direct binds for values (by declaration order) with *extra steps* (ask if not given, etc.).
Let's add them to our command

.. code-block:: python

    from ezcliy import *


    class SmallTextProcessor(Command):
        first_word = Positional('fw')
        verbose = Flag('-v', '--verbose')
        verbosity_level = KeyVal('--verbose-level', default='info')

        def invoke(self):
            if self.verbose:
                print(f'Logging enabled, {self.verbosity_level.value=}')
            print(f'You have passed {len(self.values)} arguments!')
            for _ in range(3):
                print(self.first_word)


    if __name__ == '__main__':
        SmallTextProcessor().cli_entry()

And response will look like that

.. code-block::

    python3 main.py first second -v --verbose-level=debug
    Logging enabled, self.verbosity_level.value='debug'
    You have passed 2 arguments!
    first
    first
    first

