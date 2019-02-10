"""
Reproducing Bug 190119a: Empty or incomplete CommandPackage =>
messy backtrace.

Leaving a commandpackage empty, then trying to invoke it with no
arguments results in a messy backtrace. We should get a useful error
message, detailing what is missing.
"""

import pytest

from greenland.cmdline.commandpackages import CommandPackage

class Example(CommandPackage):
    pass

@pytest.mark.bug
def test_190119a():

    Example(argv=['example']) # => messy backtrace

@pytest.mark.bug
def test_190119a_unknown_subcommand():
    from greenland.cmdline.parsers import CommandLine
    
    # this works, actually
    
    with pytest.raises(CommandLine.ErrorInContext, match="unknown subcommand"):
        Example(argv=['example','foo'])
    
