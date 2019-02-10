# * Copyright (C) 2018 M E Leypold, GPL3-or-later licensed ------------------------|
#
#   greenland.parsing.test.master_regex -- Tests for greenland.parsing.master_regex 
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

# *   Test

from ..master_regex import MasterRe

def test_master_regex():

    mre = MasterRe(
        [ ("([a-z])[a-z0-9]*", lambda m,i: ('ID',m,i)),
          ("[+*/-]",           lambda m,i: ('OP',m,i)),
          ("[0-9]+",           lambda m,i: ('NUM',m,i))
          
        ]
    )

    def match(s):
        l,(t,_,i) = mre.match(s)
        return t,l,i
    
    assert match('foo')        == ('ID',3,1)
    assert match('foo+bar')    == ('ID',3,1)
    
    assert match('3131')       == ('NUM',4,4)
    assert match('3131 * FOO') == ('NUM',4,4)

    assert match('* FOO') == ('OP',1,3)
    
