#
#   Greenland -- a Python based scripting environment.
#   Copyright (C) 2015-2017  M E Leypold.
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation; either version 2 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
#   02110-1301 USA.


"""
This suite test :py:mod:`toolbox.predicates`.

.. For more information, see: predicates.rst
"""


def create_predicates():

    """
    Create predicates by various means, provide them to the tests.
    """

    from greenland.toolbox.predicates import predicate, Predicate

    #                                          # BEGIN: wrapping a callable
    odd   = predicate(lambda x: x % 2 == 1)    # wrapping a callable
    #                                          # END.

    #                                          # BEGIN: 'predicate' as decorator
    @predicate                                 # 'predicate' as decorator
    def even(x):
        return x % 2 == 0
    #                                          # END

    #                                          # BEGIN: subclassing 'Predicate'
    class dividable_by (Predicate):

        def __init__(self, divisor):
            self.divisor = divisor

        def __call__(self, value):
            return (value % self.divisor) == 0
    #                                          # END

    #                                          # EXAMPLE:greater
    class greater(Predicate):

        def __init__(self, limit):
            self.limit = limit

        def __call__(self, value):
            return value > self.limit
    #                                          # END

    return odd, even, dividable_by, greater


def test_predicate_creation2():
    """
    This test checks and demonstrates creation of predicates by
    various methods.

    - Functional style wrapping with :py:func:`predicate`.
    - By decorator :py:func:`predicate`.
    - By subclassing from :py:class:`Predicate`.
    """

    odd, even, dividable_by, greater = create_predicates()

    #                                   # BEGIN: test_predicate_creation2, checking
    assert even(16)
    assert not even(19)

    assert odd(17)
    assert not odd(20)

    assert (dividable_by(3))(6)         # that looks strange

    dividable_by_3 = dividable_by(3)    # will look better with that

    assert dividable_by_3(6)
    assert not dividable_by_3(7)

    assert (greater(5))(6)
    #                                   # END


def compose_predicates():

    _, even, dividable_by, greater = create_predicates()

    #                                      # BEGIN:negation
    def less(x):
        return ~ greater(x - 1)
    #                                      # END

    #                                      # BEGIN:conjunction
    def in_range(x, y):
        return (~less(x)) & (~greater(y))
    #                                      # END

    #                                      # BEGIN:disjunction
    def in_range2(x, y):
        return ~(less(x) | greater(y))
    #                                      # END

    #                                      # BEGIN: test_operators, checking

    return less, in_range, in_range2


def test_operators():

    """
    This test tests composition of predicates by the redefined bitwise
    operators.
    """

    less, in_range, in_range2 = compose_predicates()

    #                                      # CHECKING: test_operators
    assert (less(5))(3)
    assert not (less(5)(6))

    assert in_range(12, 16)(16)
    assert in_range(12, 16)(12)
    assert in_range(12, 16)(15)

    assert not (in_range(12, 16)(11))
    assert not (in_range(12, 16)(17))

    assert in_range2(12, 16)(16)
    assert in_range2(12, 16)(12)
    assert in_range2(12, 16)(15)

    assert not (in_range2(12, 16)(11))
    assert not (in_range2(12, 16)(17))

    #                                      # END


def test_right_side_operators():

    """
    This test tests composition with the bitwise operators in case the
    left side operand do not derive from :py:class:`Predicate`, thus
    don't have methods `__and__` or `__or__` implemented. Dispatch in
    those cases goes over the method `__rand__` or `__ror__` respectively of the
    right side operand.
    """

    _, in_range, _ = compose_predicates()

    #                                   # BEGIN: function operand
    def odd(x):                         # a function, no instance of predicate
        return (x % 2 == 1)
    #                                   # END

    #                                   # BEGIN: right side conjunction
    def odd_and_in_range(x, y):
        return odd & in_range(x, y)
    #                                   # END

    #                                   # BEGIN: right side disjunction
    def odd_or_in_range(x, y):
        return odd | in_range(x, y)
    #                                   # END

    #                                          # CHECKING: test_right_side_operators
    assert(callable(odd_and_in_range))

    assert odd_and_in_range(12, 16)(13)        # both (internal) operands true
    assert not (odd_and_in_range(12, 16)(12))  # in_range false
    assert not (odd_and_in_range(12, 16)(11))  # in_range true

    assert(callable(odd_or_in_range))

    assert (not odd_or_in_range(12, 16)(10))   # both (internal) operands false
    assert odd_or_in_range(12, 16)(12)         # in_range true
    assert odd_or_in_range(12, 16)(11)         # odd true
    #                                          # END


def test_alternative_operators():

    """
    This test checks the alternative operators :code:`NOT`, :code:`<<AND>>` and :code:`<<OR>>`.
    """

    _, _, _, greater = create_predicates()
    less, _, _       = compose_predicates()

    from greenland.toolbox.predicates import NOT, AND, OR

    # The operator '<<AND>>' means conjunction, 'NOT' means negation.

    #                                               # BEGIN: alternative conjunction
    def in_range3(x, y):
        return NOT(less(x)) <<AND>> NOT(greater(y)) # 
    #                                               # END

    #                                               # BEGIN: alternative disjunction
    def in_range4(x, y):
        return NOT (less(x) <<OR>> greater(y))      #
    #                                               # END

    #                                               # CHECKING: test_alternative_operators
    assert in_range3(12,16) (16)
    assert in_range3(12,16) (12)
    assert in_range3(12,16) (15)

    assert not (in_range3(12,16) (11))
    assert not (in_range3(12,16) (17))

    assert in_range4(12,16) (16)
    assert in_range4(12,16) (12)
    assert in_range4(12,16) (15)

    assert not (in_range4(12,16) (11))
    assert not (in_range4(12,16) (17))
    #                                               # END
