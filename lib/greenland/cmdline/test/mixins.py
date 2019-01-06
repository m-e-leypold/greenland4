# * Copyright (C) 2018 M E Leypold, GPL3-or-later licensed -----------------------|
#
#     Tests for greenland.cmdline.mixins.
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

# *   Imports  -------------------------------------------------------------------|

from ..parsers import CommandLine, nothing, OptionsAndPosArgsParser

from greenland.toolbox.structs import Struct
from greenland.cmdline.tools import flag

import pytest
import textwrap

from .parsers import options_spec_1, posargs_spec_1

# * CommandParser

from ..mixins import CommandParser, MergeArguments

def test_mixins_spike():


    class Parser(MergeArguments,CommandParser):
        
        def parse(self,tokens):
            arguments = super().parse(tokens)
            assert len(arguments) == 1
            return arguments[0]

    
    parser = Parser(options_spec_1,posargs_spec_1)
    
    def parse(*args):

        with CommandLine(['$PROGRAM']+list(args)) as tokens:
            nonlocal parser
            r = parser.parse(tokens)
            return r, len(list(tokens))

    assert  parse('-f','l1','l2','0.3','0.4') == ({'l1': 'l1', 'l2': 'l2', 't3': 0.3, 't4': 0.4, 'v': [], 'force': True}, 0)
    assert  parse('l1','l2','-f','0.3','0.4') == ({'l1': 'l1', 'l2': 'l2', 't3': 0.3, 't4': 0.4, 'v': [], 'force': True}, 0)
    assert  parse('l1','l2','0.3','0.4','-f') == ({'l1': 'l1', 'l2': 'l2', 't3': 0.3, 't4': 0.4, 'v': [], 'force': True}, 0)

    with pytest.raises(CommandLine.ErrorInContext) as info:
        parse('-f','--')

    assert str(info.value) == textwrap.dedent("""

      $PROGRAM: CommandLine.ErrorInContext:
          $PROGRAM -f --
                      --
          expected end of arguments here."""
    )

# * SubcommandPackageParser
    
from ..mixins import SubcommandPackageParser

def test_subcommand_package_spike():

    none = Struct( name = None, aliases = [], parser = nothing )

    foo = Struct( name = 'foo', aliases = ['f','FOO'],
                   parser = OptionsAndPosArgsParser([
                       Struct( name='force', aliases = ['f'], key="force",  implied_value=True, convert = flag ),
                       Struct( name='alpha', aliases = ['a'], key="alpha",  convert = float )
                   ])
    )

    bar = Struct( name = 'bar', aliases = ['b'],
                   parser = OptionsAndPosArgsParser([
                       Struct( name='beta', aliases = ['b'], key="beta", convert = int ),
                   ])
    )

    subcommands_spec = [ none, foo, bar ]
    
    parser = SubcommandPackageParser(options_spec_1,subcommands_spec)
    
    def parse(*args):

        with CommandLine(['$PROGRAM']+list(args)) as tokens:
            nonlocal parser
            r = parser.parse(tokens)
            if len(r)>=4:
                r[3] = [ token.lexeme for token in r[3]]
        return r, len(list(tokens))

    assert  parse('-f','foo','-a','3')     == ([ { 'force':True }, foo, { 'alpha':3 }, [] ], 0)
    assert  parse('-f','foo','-a','3','x') == ([ { 'force':True }, foo, { 'alpha':3 }, ['x'] ], 0)
    
    assert  parse('-f') == ([ { 'force':True }, none], 0)
    assert  parse()     == ([ {}, none], 0)

    
    with pytest.raises(CommandLine.ErrorInContext) as info:
        parse('-f','foo','-a','3','x','--')

    assert str(info.value) == textwrap.dedent("""

      $PROGRAM: CommandLine.ErrorInContext:
          $PROGRAM -f foo -a 3 x --
                                 --
          expected end of arguments here."""
    )

        
