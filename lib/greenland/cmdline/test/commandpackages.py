# * Copyright (C) 2018 M E Leypold, GPL3-or-later licensed  ----------------------|
#
#   Tests of greenland.cmdline.commandpackages
#   Copyright (C) 2018 M E Leypold
#
#   This program is free software: you can redistribute it and/or
#   modify it under the terms of the GNU General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see
#   <https://www.gnu.org/licenses/>.
#

# *   Imports  -------------------------------------------------------------------|

from ..commandpackages import *
from greenland.toolbox.structs import Struct

# *   Fixtures  ------------------------------------------------------------------|

class Foo(CommandPackage):
    
    """
    Foo Subcommands Package, (C) 2018 M E Leypold

    Usage: foo [$OPTIONS...] $COMMAND [$SUBCOMMAND-OPTIONS...] $ARGUMENTS...
           foo --help

    Execute $COMMAND.
    """

    options = [
        Option ( 'root', ['r'], str, "path to the database" ),
        Flag   ( 'force', ['f'], "force otherwise inhibited operation" ),
    ]


    @subcommand (
        
        "greet", ['g'], "greet the user", usage = [
        
            Flag   ('enthusiastic',['e'], "perform the greeting enthusiasically"),
            Option ('strength', ['s'], float, "strength of greeting", default=2.4),
        
            Required('whom',str,"whom to greet")
    ])    
    def greet(self,whom,enthusiastic,strength):
        self.saved = Struct(__command__="greet", whom=whom,enthusiastic=enthusiastic,strength=strength)
    
    @subcommand ( "check", ['c'], "check database", [
        Flag ('report',['r'], "write report to stdout")
    ])    
    def check(self,report):
        self.saved = Struct(__command__="check", report=report)
        

    @subcommand ( None, ['h','help'], "show help page")
    def help(self):
        self.saved = Struct(__command__="help")

# *   Testing CommandsPackage  ---------------------------------------------------|
        
def test_commandspackage():
    
    foo1 = Foo(argv=['foo','greet','-e','George'])
    assert foo1.saved == Struct(__command__="greet", whom='George',enthusiastic=True,strength=2.4)

    foo2 = Foo(argv=['program'])
    assert foo2.saved == Struct(__command__="help")
    
