# * Copyright (C) 2018 M E Leypold, GPL3-or-later licensed  --------------------|
#
#     greenland.filesystem.test.trees -- Unit tests for greenland.filesystem.trees
# 
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
#

# * Imports  -------------------------------------------------------------------|

import pytest

from ..trees import FSObject, RootPathInfo, find, find_files

# * Fixture  -------------------------------------------------------------------|

def create_filetree_fixture(root,layout):

    def touch(path):
        with open(path,'w') as f: pass
    
    for key,content in layout.items():
        
        if (content == None):
            touch(root.join(key))
            continue

        if type(content) == str:
            with open(root.join(key),'w') as f:
                f.write(content)
            continue

        
        if type(content) in [list,dict]:
            subdir = root.join(key)        
            subdir.mkdir()
            
            if type(content) == list:
                for name in content:
                    touch(subdir.join(name))
                continue
            
            if type(content) == dict:
                create_filetree_fixture(subdir,content)                    
                continue
            
        
@pytest.fixture
def filetree1(tmpdir):

    layout = {
        'a'   : [ 'b.txt', 'c.txt' ],
        'x'   : [ 'y.md', 'x.org' ],
        'foo' : 'content-foo',
        's'   : {
            'u' : None,
            'v' : None,
            'z' : ['z1','z2','z3']
        }
    }

    root = tmpdir.join("filetree1")

    root.mkdir()
    create_filetree_fixture(root,layout);
    
    yield str(root)
    return

# * Tests  ---------------------------------------------------------------------|

def test_spike(filetree1):

    def find_paths( accept=lambda obj: True):
        return { obj.relpath for obj in find(filetree1, accept = accept) }
    

    def find_parents( accept=lambda obj: True):
        return { (obj.parent.relpath if obj.parent != None else None)
                 for obj in find(filetree1, accept = accept) }
    
    assert find_paths( lambda obj: obj.ext == "txt" ) == {'a/b.txt', 'a/c.txt'}
    
    assert find_paths() == {
        '.','s', 'a', 'foo', 'x',
        'x/x.org', 'x/y.md', 's/u','s/v', 's/z', 'a/c.txt', 'a/b.txt',
        's/z/z1', 's/z/z2', 's/z/z3'
    }
    
    assert find_parents( lambda obj: obj.ext == "txt" ) == {'a'}

    assert find_parents() == {
        None, '.', 'x', 's', 'a', 's/z'
    }    


    def find_dirs_and_files( accept=lambda obj: True):
        dirs  = set()
        files = set()

        for obj in find_files(filetree1, accept=accept, accept_parents = True):
            if obj.is_dir:
                dirs.add(obj.relpath)
            else:
                files.add(obj.relpath)

        return dirs,files

    assert find_dirs_and_files(lambda obj: obj.ext == "txt") == (
        {'.','a'}, {'a/b.txt', 'a/c.txt'}
    )
                        

        
