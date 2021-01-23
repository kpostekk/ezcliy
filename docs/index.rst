.. ez cliy documentation master file, created by
   sphinx-quickstart on Thu Jan 14 17:39:56 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

**ez cliy** docs
===================================
An alternative framework for click or argparse.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   firststeps
   click
   command
   parameters

Features
---------
* Model-like decarating of parameters and values
* Easy command nesting
* Async support
* *not yet, but i'm planning to add fish and zsh code completion generator*

Install
--------

.. code-block::

   pip3 install git+https://github.com/kpostekk/ezcliy.git

Example
--------

.. code-block:: python

   from ezcliy import Command, Flag  # Import required classes


   class SmallTextProcessor(Command):
       # Define excpected flags
       capitalize = Flag('-c', '--capitalize')
       verbose = Flag('--verbose')

       def invoke(self):  # There put your sweet code
           string = ' '.join(self.values)
           if self.verbose:
               print('Verbose stuff', self.parameters, self.values)
           if self.capitalize:
               string = string.capitalize()
           if not string.endswith('.'):
               string += '.'
           print(string)


   if __name__ == '__main__':
       SmallTextProcessor().cli_entry()

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
* :ref:`modindex`
