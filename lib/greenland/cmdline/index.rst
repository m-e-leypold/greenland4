.. Copyright © 2018,  M E Leypold.

   Permission is granted to copy, distribute and/or modify this
   document under the terms of the GNU Free Documentation License,
   Version 1.3 or any later version published by the Free Software
   Foundation; with no Invariant Sections, no Front-Cover Texts, and
   no Back-Cover Texts.  A copy of the license is included in the
   section entitled "GNU Free Documentation License".

   
Commandline Applications
========================

`Greenland` makes it possible to define command line applications from
a high level specification. In example, the following file

.. literalinclude:: example/greet.py
   :start-after:    # begin-example
   :end-before:     # end-example		    
		    		  
defines an indispensable utility for advance teams of alien
invaders. It takes an optional positional parameter (whom to greet)
with a default (``'people'``), a flag ``'-l'`` to add the line
``'Bring me to your leader!'``, and an option ``'-p'`` to change the
appellation used for greeting (per default it is ``'hello'``).

The parsers for the command line interface are created when the class
``Greet`` is being defined (so error in the definitions mostly turn up
when loading the file, not later when running the application).

Instantiating ``Greet`` will pick the argument vector from ``sys``,
parse it according to the definition given, squirrel away the option
arguments into instance variables (``leader`` and ``phrase``) and
passe the positional arguments to ``main``. If a error occurs while
parsing the command line, the error is pretty printed, like this,

.. code-block:: shell
   
   ./greet.py: CommandLine.ErrorInContext:
       ./greet.py -x
		  --
       unknown option.

and the program exists.

The resulting application also understands long options in GNU and in
X11 style (``--leader``, ``--phrase`` as well as ``-leader`` and
``-phrase``), and special cases for disabling the flag
(e. g. ``-no-leader``, ``+l`` or ``--leader=false``). All those fall
out of the command line parsing framework basically for free.

``Greet`` (the class) can also take a number of optional parameters
that make testing easier (e. g. one does probably not want to exit the
process when instantiating the application class in a test).

.. py:module::  greenland.cmdline.specification

All command line parsing utilities are located under the hierarchy
:py:mod:`greenland.cmdline`.

- Module :py:mod:`shellcommands` provides the mechanisms demonstrated
  above that enable the user to create a simple command line
  interface. 

- Module :py:mod:`commandpackages` enables creation of "svn style"
  command line interfaces (i. e. interfaces which accept global
  options, a command name and the options and positional arguments
  specific to this command).

- Module :py:mod:`scriptomatic` also enables creation of simple
  command line interfaces (no sub-commands) as
  :py:mod:`shellcommands`, but with the difference that there is no
  class that represents the application: Instead functions as globals
  in a file make up the application.

Details are provided later in this chapter.
      
.. note::
   
   The documentation strings in the example suggest that there should
   be a way to print a help page that might be composed automatically
   from the documentation strings. This is, unfortunately, not the
   case, **yet**.


Some Definitions
----------------

Before we go into further details, it is necessary to define some
concepts and terms we will use to talk about command line
interfaces. Unfortunately it seems quite common in documentation
regarding command line interfaces that e. g. the concepts parameters
and arguments are mixed up which makes for less than understandable
explanation when talking e. g. about how user input is mapped to data
that is further processed by some program.

Parameters and Arguments
........................

(more to come)

   
   

		
