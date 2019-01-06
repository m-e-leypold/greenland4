# * Copyright (C) 2018 M E Leypold, GPL3-or-later licensed -----------------------|
#
#     Tests for scriptomatic.
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

from . import example_scriptomatic_p1 as p1
from ..scriptomatic import run_script

import sys

# *   Test  ----------------------------------------------------------------------|

def test_running_scriptomatic_script():
    run_script(p1.__dict__,['PROGRAM','-a','5','x'])
    assert p1.option.alpha == 5
    assert p1.target_saved == 'x'
    
