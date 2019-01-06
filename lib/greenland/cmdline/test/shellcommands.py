# * Copyright (C) 2018 M E Leypold, GPL3-or-later licensed -----------------------|
#
#     Tests for greenland.cmdline.shellcommands
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


from ..shellcommands import *
from greenland.toolbox.structs import Struct
from pytest import raises

import textwrap

class Foo(ShellCommand):

    """
    Foo Sample Script, (C) 2018 M E Leypold

    Usage: foo $OPTIONS $ARGUMENTS
           foo --help

    Foonify the given target with the provided parameters.
    """

    option_struct = 'option'

    usage = [
        Option ( 'queue', ['a'], int, "filter queue size" ),
        Flag   ( 'force', ['f'], "force otherwise inhibited operation" ),
        
        Required ('target', str,"target identifier"),
        Optional ('relay', str, "relay identifier" )
    ]
    
    def main(self,target,relay=None):

        self.saved = Struct(target=target,relay=relay)


class Bar(Foo):
    option_struct = None
    
        
def test_shellcommand():

    foo = Foo(argv=['program','-a','5','x','r'])
    assert foo.saved  == Struct(target='x',relay='r')
    assert foo.option == Struct(queue=5,force=False)
    
    with raises(UserError) as info:
        Foo(argv=['program','-a','5'],exit_on_error=False)

    assert str(info.value) == textwrap.dedent("""

        program: CommandLine.ErrorInContext:
            program -a 5    
                         ---
            not enough arguments."""
    )

    print()
    with raises(SystemExit):
        Foo(argv=['program','-a','5'])    


    bar = Bar(argv=['program','-a','5','x','r'])
    assert bar.saved == Struct(target='x',relay='r')
    assert bar.queue == 5
    assert bar.force == False
