Greenland: Pythonic Infrastructure
==================================

Greenland is a package that lowers the entry barrier to implementing
tasks that are often more typically done in shell scripts.

Source code is available from the `git repository`_. See
`CHANGELOG.rst`_ for changes and release history.

.. _CHANGELOG.rst:  file:CHANGELOG.rst
.. _git repository: https://github.com/m-e-leypold/greenland4


The example given below showcases what Greenland purports to solve: To
provide easily composable building blocks for tasks that occur in
areas commonly reserved to shell scripting.

Greenland currently is not complete in this respect and will not be
for some time. The author regardless wishes users much fun and
success, in case they decide to use Greenland.


An example
----------

Assume, you're tasked with writing a utility for cleaning up directory
trees. It should allow th user to provide a pattern and a directory
path, then all files matching this pattern are deleted in the
referenced directory tree, like this:

.. code-block:: console
   
   $> rm-in-tree '*~' my/data

The obvious and probably cheapest solution -- if you're fluent in bourne shell and shell
utilities, is, to build a shell script around a line like

.. code-block:: console

   find "$ROOT" -name "$PATTERN" -print0 | xargs -0 rm -f

It still leaves you with the burden to do some command line parsing in
shell script -- which is not overly heavy in this case so far, but
spins quickly out of control when the client wants more features, like:

- A configuration for the default pattern in the users home directory.
- A verbose option to log the parameters given and the files deleted.
- A dry-run option to preview what will be deleted.

Sooner or later you'll wish you could do that in a real programming
language where not all data types are strings that are pasted together
by arcane expansion rules.

So, this would be a case to use in example Python. While handling data
in a real programming language is clearly less flakey than in the
shell, parsing command lines often still constitutes a major burden,
even with helpers already in the standard libraries. This is also true
for Python. And finding files in directory tree is also a bit of an
effort.

So what the author of Greenland would have liked is to have in Python
all the building blocks that one normally has available in shell
programming, but where possible, better (like in example the command
line parsing, which IMHO turns out to be a mess in practically all
appoaches I've seen so far).

So, what what the author of Greenland would have liked to have, is a
declarative way of specifying the command line arguments, like in

.. literalinclude:: examples/rm-in-tree/rm-in-tree
   :language: python
   :start-after: [manual] begin usage
   :end-before: [manual] end usage
   :dedent: 4

And the author of Greenland would have like to have a simple way to
iterate over all the files in a directory tree with a specified
property, like in
		
.. literalinclude:: examples/rm-in-tree/rm-in-tree
   :language: python
   :start-after: [manual] begin find_files
   :end-before: [manual] end find_files
   :dedent: 8

You can also see, how the *dry-run* option has become an object member
variable here. This is done automagically by the Greenland algorithms,
except if you specify otherwise.

LICENSE
-------

Greenland is free Software and licensed by the terms of the Gnu Public
License, version 3 or later (GPL3).

For details and the full license text see the file LICENSE.txt at the
top of the source tree.


