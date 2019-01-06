# *   Copyright (C) 2018 M E Leypold, GPL3-or-later licensed -----------------------|
#
#     Test for greenland.toolbox.structs
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

# *   Preamble + Infrastructure ----------------------------------------------------|

import pytest


# *   Tests ------------------------------------------------------------------------|

def test_structs():
    
    from ..structs import Struct

    s1 = Struct(foo="abc",bar="xyz")

    assert hasattr(s1,"foo") and s1.foo == "abc"
    assert hasattr(s1,"bar") and s1.bar == "xyz"    

    # TODO: There is no test that structs can be compared on quality
