# * Copyright (C) 2018 M E Leypold, GPL3-or-later licensed -----------------------|
#
#     Tests for greenland.cmdline.tools
#     Copyright (C) 2018 M E Leypold
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

# *   Preamble ---------------------------------------------------------------------|

from   greenland.conventions   import longstr
from   greenland.cmdline.tools import ArgvPreProcessor, flag, extract_lexemes

import pytest
from   pytest import raises, mark
import re

from greenland.toolbox.structs import Struct


Spec = Struct

# **  ------------------------------------------------------------------------------|
# *   Preprocessing Tests ----------------------------------------------------------|
# **  ------------------------------------------------------------------------------|
# **  Infrastructure (Preprocessing Tests)------------------------------------------|

def check(lexeme,label=None,value=None, sep = False, posarg = False ):
    
    token = ArgvPreProcessor().match(lexeme)

    assert token.is_separator == sep
    assert isinstance(token,ArgvPreProcessor.PositionalArgument) == posarg

    if label != None:
        assert token.is_option
        assert token.label == label
        if value != None:
            assert token.carries_value
            assert token.value == value
        else:
            assert not token.carries_value
    else:
        assert not token.is_option
        assert not token.carries_value

# **  Test Preprocessing -----------------------------------------------------------|

def test_preprocessing():

    # classic options
    # ---------------
    #
    # Classical options don't carry a value. Any value it will have to
    # follow in the next argument. It depends on the option semantics
    # if the option will be parsed as flag (value implied) or a
    # key-value pair (value follows in next argument). Preprocessing
    # does not make any difference between classic flags and classic
    # key/value pairs and between short single letter and X11 style
    # long option.
    #

    check( "-abc",label="abc")
    check( "-a",  label="a"  )

    # gnu style key/value pairs
    # -------------------------
    #
    # Those carry their values in the argument string. The pre
    # processor will provide them as attribute label.

    check( "--abc=xyz", label="abc", value = "xyz" )
    check( "--a=xyz",   label="a",   value = "xyz" )
    check( "--a=xy=z",   label="a",  value = "xy=z" )

    check( "--abc=", label="abc", value = "" )
    check( "--a=",   label="a",   value = "" )

    # gnu style flags
    # ---------------
    #
    # Those carry an implied value with them: The string 'True'.
    
    check( "--abc", label="abc", value = 'True' )    # implied value is a string here
    check( "--a",   label="a", value = 'True'   )

    # PositionalArg
    # ---------------
    #

    check( "abc", posarg = True )
    check( "a",   posarg = True )

    check ("",    posarg = True)
    check ("-",   posarg = True)         # ditto

    # The double dash separator
    # ---------------
    #

    check( "--", sep = True )

    # Extensions
    # ---------------
    #

    check( "-no-abc", label = 'abc', value = "False" )
    check( "--no-abc", label = 'abc', value = "False" )


# **  ------------------------------------------------------------------------------|
