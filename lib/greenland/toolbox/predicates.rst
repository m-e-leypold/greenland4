.. Copyright © 2018,  M E Leypold.

   Permission is granted to copy, distribute and/or modify this
   document under the terms of the GNU Free Documentation License,
   Version 1.3 or any later version published by the Free Software
   Foundation; with no Invariant Sections, no Front-Cover Texts, and
   no Back-Cover Texts.  A copy of the license is included in the
   section entitled "GNU Free Documentation License".

   
Predicates
==========

.. automodule:: greenland.toolbox.predicates

Composing two predicates `p` and `q` with, in example, `&` as follows

.. code-block:: python

   r = p & q

allows to express more concisely and with less clutter what usually
would be written as

.. code-block:: python

   r = lambda x: p(x) && q(x)

On the down side pointfree notation is less usual, so using one or the
other style is a matter of preference. `toolbox.predicates` provides
the composition operators `&`, `|`, `~` for logical *and*, *or* and
*not* operations. It also provides a class :py:class:`Predicate` that
can be used as *decorator*, in example

.. code-block:: python

   from toolbox.predicates import predicate

   @predicate
   def positive(x):
       return x>0

or which can be derived from, in example to create families of
predicates with parameters, as in


.. code-block:: python

   from toolbox.predicates import Predicate

   class greater (Predicate):

	def __init__ (self, limit):
	    self.limit = limit

	def __call__ (self, value):
	    return value>self.value

    # ...

    blabla.filter( condition = greater(11) & smaller(20) )

`toolbox.predicates` also provides the composition operators as
identifiers (partially using the *infix* package): :code:`NOT`,
:code:`<<AND>>`, and :code:`<<OR>>`. An example:

.. code-block:: python

   r = NOT( p <<AND>> q )

These :ref:`alternative operators
<predicate_alternative-operators>` exist for application areas and
users where it is felt that overloading of the bitwise operators as
explained above would only further confusion.


Decorator predicate
-------------------

.. autofunction:: predicate

		 
Class Predicate
---------------

.. autoclass:: Predicate
	       
Example
.......

.. literalinclude:: test/predicates.py
   :start-after:    EXAMPLE:greater
   :end-before:     END
   :dedent:         4


Composition Operators
---------------------


.. _predicate_bitwise-operators:

Redefined bitwise Operators
...........................

The module implements the bitwise operators `&`, `|` and
`~` as pointfree_ composition operators on class
:py:class:`Predicate`. Both, the `left-side`_ and the right-side_
version of the binary operators are implemented, so to use them only
one of the operators has to be derived from :py:class:`Predicate`.

.. _`right-side`: https://docs.python.org/3/reference/datamodel.html?highlight=__rand__#object.__rand__
.. _`left-side`: https://docs.python.org/3/reference/datamodel.html?highlight=__and__#object.__and__

(*Rationale* for the decision to use the bitwise operators: In Python
one cannot redefine the boolean operators).

A :ref:`tabular overview <predicate_composition-operator-table>` of the
operators with example snippets has already been given :ref:`above
<predicate_composition-operator-table>`.

With the operators `&`, `|` and `~` at least one of the operators must
be subclass of :py:class:`Predicate`, but it suffices if at least one
of them is of a subclass of :py:class:`Predicate`.

.. _predicate_alternative-operators:

Alternative (Identifier) Operators
....................................

Module :py:mod:`toolbox.predicates` also provides the composition
operators as identifiers (partially using the infix_ package):
:code:`NOT`, :code:`<<AND>>`, and :code:`<<OR>>`. These
:ref:`alternative operators <predicate_alternative-operators>` exist
for application areas and users where it is felt that overloading of
the bitwise operators as explained above would only further confusion.

Furthermore with :samp:`NOT`, :samp:`<<AND>>`, and :code:`<<OR>>`,
none of the operands need to be a subclass of :py:class:`Predicate`,
though the result is indeed a subclass of :py:class:`Predicate`.

A :ref:`tabular overview <predicate_composition-operator-table>` of the
operators with example snippets has already been given :ref:`above
<predicate_composition-operator-table>`.

.. _infix: https://pypi.org/project/infix/


