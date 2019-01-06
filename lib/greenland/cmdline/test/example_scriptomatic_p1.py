# * Copyright (C) 2018 M E Leypold, GPL3-or-later licensed -----------------------|
#
#     Example for a scriptomatic script.
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

# * Example ----------------------------------------------------------------------|

"""
A sample script -- (C) 2018, M E Leypold

More text and more text. The future will be to use this to print help
pages, but currently there are no help pages.
"""

from greenland.cmdline.scriptomatic import *

usage = [

    Option ("alpha", ['a'], int, "rotation angle"),
    Flag   ("force", ['f'], "force operation"),

    Required ("target", str, "operation target")
]


def main(target):
    print("----------")
    print(option)
    print(target)
    print("----------")    

    global target_saved
    target_saved = target

    
if __name__ == '__main__':
    run_script(globals())
