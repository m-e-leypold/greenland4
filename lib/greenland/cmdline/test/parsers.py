# * Copyright (C) 2018 M E Leypold, GPL3-or-later licensed  ----------------------|
#
#   greenland.cmdline.tests.parsers -- Testing greenland.cmdline.parsers
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

from abc import abstractmethod
from more_itertools import peekable

import pytest
from   pytest import raises

import textwrap
from greenland.cmdline.tools import preprocessed, underline, flag
from greenland.conventions import longstr
from greenland.toolbox.structs import Struct

from .. import parsers

# *   Tools  ---------------------------------------------------------------------|

from ..parsers import maybe_to_specmap

def test_to_specmap():
    d = { 1:2, 3:4 }
    assert id(maybe_to_specmap(d)) == id(d)

    i1 = Struct(name="foo",aliases=['f','FOO'])
    i2 = Struct(name="bar",aliases=['b','BAR'])

    d = [ i1, i2 ]

    assert maybe_to_specmap(d) == { 'foo' : i1, 'FOO' : i1, 'f' : i1,
                                    'bar' : i2, 'BAR' : i2, 'b' : i2
    }

# *   CommandLine Context --------------------------------------------------------|

from greenland.conventions import UserError
from ..parsers import CommandLine


def test_error_rewriting():
    
    args = ['program','-a','-q','foo']

    with pytest.raises(UserError) as info:
        with CommandLine(args) as tokens:
            i = 0
            for token in tokens:
                i += 1
                if (i==2):
                    raise CommandLine.Error("offending token",[token,next(tokens)])

    assert str(info.value) == textwrap.dedent("""
    
        program: CommandLine.ErrorInContext:
            program -a -q foo
                       -- ---
            offending token."""
    )


    with pytest.raises(CommandLine.ErrorInContext) as info:
        with CommandLine(args) as tokens:
            raise CommandLine.Error("expected something here",None)

    assert str(info.value) == textwrap.dedent("""
    
        program: CommandLine.ErrorInContext:
            program -a -q foo    
                              ---
            expected something here."""
    )


def test_error_rewriting_start_0():
    
    args = ['-a','-q','foo']

    with pytest.raises(CommandLine.ErrorInContext) as info:
        with CommandLine(args,start=0,program='program') as tokens:
            i = 0
            for token in tokens:
                i += 1
                if (i==1):
                    raise CommandLine.Error("offending token",[token,next(tokens)])

    assert str(info.value) == textwrap.dedent("""
    
        program: CommandLine.ErrorInContext:
            -a -q foo
            -- --    
            offending token."""
    )


    with pytest.raises(CommandLine.ErrorInContext) as info:
        with CommandLine(args,start=0,program='program') as tokens:
            raise CommandLine.Error("expected something here",None)

    assert str(info.value) == textwrap.dedent("""
    
        program: CommandLine.ErrorInContext:
            -a -q foo    
                      ---
            expected something here."""
    )

# *   Parsers  -------------------------------------------------------------------|
# **   OptionsProcessor

from ..parsers import BaseParser, OptionsProcessor, append_to_list

    
options_spec_1 = [
    Struct( name='force', aliases=['f'], key="force",  implied_value=True, convert = flag ),
    Struct( name='debug', aliases=['d'], key="debug",  implied_value=True, convert = flag ),
    Struct( name='alpha', aliases=['a'],  key='alpha', convert=int ),
    Struct( name='beta',  aliases=['b'],  key='beta',    convert=float ),
    Struct( name='include', aliases=['I'], key='include', merge=append_to_list)
]

        
def test_spike_options_processor():

    spec = options_spec_1

    
    KwArg      = OptionsProcessor.KwArg
    PosArg     = OptionsProcessor.PosArg
    Separator  = OptionsProcessor.Separator

    processor = OptionsProcessor(spec)


    def unpack(item):
        if item.__class__ == Separator: return Separator
        if item.__class__ == PosArg:
            return (PosArg,item.value)
        if item.__class__ == KwArg:
            return (KwArg,item.key,item.value)
        assert False
        
    def process(*args):
        with CommandLine(['$PROGRAM']+list(args)) as tokens:                
            results = [ unpack(result) for result in processor.process(tokens) ]
        return results

    assert process()     == []
    assert process('-f')                  == [ (KwArg,'force',True) ]
    assert process('-f','a')              == [ (KwArg,'force',True), (PosArg,'a') ]
    assert process('-f','a','-alpha','5') == [ (KwArg,'force',True), (PosArg,'a'), (KwArg,'alpha',5)]

    assert process('-f','a','-alpha','5','--','b') == [
        (KwArg,'force',True), (PosArg,'a'), (KwArg,'alpha',5), Separator, (PosArg,'b')
    ]

    assert process('a','-alpha','5','--','b') == [
        (PosArg,'a'), (KwArg,'alpha',5), Separator, (PosArg,'b')
    ]

    assert process('--','b') == [ Separator, (PosArg,'b') ]
    assert process('--') == [ Separator ]

    # TODO: Test proper triggering of error cases (e58a1f11-97a4-439e-937c-a6c503965b3d)

    with pytest.raises(CommandLine.ErrorInContext) as info:
        process('-alpha','z')

    assert str(info.value) == textwrap.dedent("""

       $PROGRAM: CommandLine.ErrorInContext:
           $PROGRAM -alpha z
                           -
           cannot convert option argument with <class 'int'>."""
    )


    with pytest.raises(CommandLine.ErrorInContext) as info:
        process('-alpha')

    assert str(info.value) == textwrap.dedent("""

       $PROGRAM: CommandLine.ErrorInContext:
           $PROGRAM -alpha    
                           ---
           expected argument after option."""
    )

    assert process('-alpha','-5') == [(KwArg,'alpha',-5)]

    with pytest.raises(CommandLine.ErrorInContext) as info:
        process('-alpha','-f')

    assert str(info.value) == textwrap.dedent("""

       $PROGRAM: CommandLine.ErrorInContext:
           $PROGRAM -alpha -f
                    ------ --
           argument to option is not a positional argument (syntactically)."""
    )

    
# **   OptionsParser

from ..parsers import OptionsParser
        
def test_spike_options_parser():

    spec   = options_spec_1
    parser = OptionsParser(spec)
        
    def parse(*args):
        with CommandLine(['$PROGRAM']+list(args)) as tokens:                
            results = parser.parse(tokens)            
        return results, [ token.lexeme for token in tokens ]



    assert parse ()             == ( {}, [] )    
    assert parse ('-alpha','5') == ( {'alpha':5}, [] )

    assert parse ('-alpha','5','--') == ( {'alpha':5}, ['--'] )
    assert parse ('-alpha','5','x')  == ( {'alpha':5}, ['x'] )
    
    assert parse ('-alpha','5','-f')  == ( {'alpha':5, 'force':True}, [] )            


    assert parse ('-I','abc','-I','xyz') == ( {'include':['abc','xyz']}, [] )

    # TODO: More systematic tests (6f6ed09e-8008-495c-aadc-9f2a15a179b6)



# **   OptionsAndPosArgsParser

from ..parsers import OptionsAndPosArgsParser

def test_spike_options_and_posargs_parser():

    spec   = options_spec_1
    parser = OptionsAndPosArgsParser(spec)
        
    def parse(*args):
        with CommandLine(['$PROGRAM']+list(args)) as tokens:                
            options,posargs = parser.parse(tokens)            
        return options,[ posarg.lexeme for posarg in posargs ] ,[ token.lexeme for token in tokens ]

    assert parse ()             == ( {}, [], [] )
    assert parse ('-a','-5')    == ( {'alpha':-5}, [], [] )
    
    assert parse ('-a','-5','x','-f','--','y') == (
        {'alpha':-5,'force':True}, ['x'], ['--','y']
    )

    assert parse ('x','y') == ( {}, ['x','y'], [] )

    # TODO: More systematic tests (b50e9e80-a80b-4f83-8b41-154b2dbfde33)
    
# **   PosArgsCollector

from ..parsers import PosArgsCollector, posargs_collector

# **   PosArgsBinder

from ..parsers import PosArgsBinder

Spec = Struct

posargs_spec_1 = Struct(
    leading           = [  Spec(key="l1"), Spec(key="l2") ],
    leading_optional  = [  Spec(key="l3opt") ],
    variadic          = Spec(key="v",min_required=0,max_allowed=None,unlimited_allowed=True,convert=int),
    trailing_optional = [  Spec(key="t1opt",convert=float),Spec(key="t2opt",convert=float) ],
    trailing          = [  Spec(key="t3",convert=float), Spec(key="t4",convert=float) ]
)


posargs_spec_2 = Struct(
    leading           = [  Spec(key="l1"), Spec(key="l2") ],
    leading_optional  = [  Spec(key="l3opt") ],
    variadic          = None,
    trailing_optional = [  Spec(key="t1opt",convert=float), Spec(key="t2opt",convert=float)  ],
    trailing          = [  Spec(key="t3",convert=float), Spec(key="t4",convert=float)  ]
)


posargs_spec_3 = Struct(
    leading           = [  Spec(key="l1"), Spec(key="l2") ],
    leading_optional  = [],    
    variadic          = None,
    trailing_optional = [],    
    trailing          = [  Spec(key="t3",convert=float), Spec(key="t4",convert=float) ]
)

def test_bind_posargs():

    def new_bind(specs):
        binder = PosArgsBinder(specs)
        Token  = Struct
        def bind(*args):
            with CommandLine(['$PROGRAM']+list(args)) as tokens:
                return binder.bind(list(tokens))
        return bind
    
    bind1 = new_bind(posargs_spec_1)
    bind2 = new_bind(posargs_spec_2)
    bind3 = new_bind(posargs_spec_3)    

    # Can bind minimum number of args
    
    assert bind1 ("a1","a2","0.3","0.4") == {'l1': 'a1', 'l2': 'a2', 't3': 0.3, 't4': 0.4, 'v': []}
    assert bind2 ("a1","a2","0.3","0.4") == {'l1': 'a1', 'l2': 'a2', 't3': 0.3, 't4': 0.4}
    assert bind3 ("a1","a2","0.3","0.4") == {'l1': 'a1', 'l2': 'a2', 't3': 0.3, 't4': 0.4}


    # Leading required parameters always take the head of the
    # arguments, trailing required parameters the tail. The arguments
    # in between are taken by leading optional parameters, leading
    # trailing optional parameters and the rest by the variadic
    # argument.
    
    assert bind1 ("a1","a2","a5", "0.3","0.4") == {'l1':'a1', 'l2':'a2',  'l3opt':'a5', 't3':0.3, 't4':0.4, 'v':[] }
    assert bind2 ("a1","a2","a5", "0.3","0.4") == {'l1':'a1', 'l2':'a2',  'l3opt':'a5', 't3':0.3, 't4':0.4 }
    
    assert bind1 ("a1","a2","a5", "0.6", "0.3","0.4") == {'l1':'a1', 'l2':'a2',  'l3opt':'a5', 't2opt':0.6, 't3':0.3, 't4':0.4, 'v':[] }
    
    assert bind1  ("a1","a2","a5", "0.6", "0.7", "0.3","0.4") == {
        'l1':'a1', 'l2':'a2',  'l3opt':'a5', 't1opt':0.6, 't2opt':0.7, 't3':0.3, 't4':0.4, 'v':[]
    } 
    
    assert  bind2 ("a1","a2","a5", "0.6", "0.7", "0.3","0.4") == {
        'l1':'a1', 'l2':'a2',  'l3opt':'a5', 't1opt':0.6, 't2opt':0.7, 't3':0.3, 't4':0.4
    }


    # variadic parameter
    
    assert  bind1 ("a1","a2","a5", "8", "0.6", "0.7", "0.3","0.4") == {
        'l1':'a1', 'l2':'a2',  'l3opt':'a5', 't1opt':0.6, 't2opt':0.7, 't3':0.3, 't4':0.4, 'v':[8]
    }
    
    assert  bind1 ("a1","a2","a5", "8", "9", "0.6", "0.7", "0.3","0.4") == {
        'l1':'a1', 'l2':'a2',  'l3opt':'a5', 't1opt':0.6, 't2opt':0.7, 't3':0.3, 't4':0.4, 'v':[8,9]
    }
    
    with pytest.raises(CommandLine.ErrorInContext) as info:    
        bind2 ("a1","a2","a5", "8", "0.6", "0.7", "0.3","0.4")

    assert str(info.value) == textwrap.dedent("""

    $PROGRAM: CommandLine.ErrorInContext:
        $PROGRAM a1 a2 a5 8 0.6 0.7 0.3 0.4
                                        ---
        too many arguments."""
    )

    # TODO: Copy more tests from older approach or develop ab initio (57b4ed66-03ff-4c46-afdd-d33f109c3423)
        
# **   PosArgsCollectorAndBinder

from ..parsers import PosArgsCollectorAndBinder

def test_posargs_collector_and_binder_spike():

    def create_new_parse(specs):        
        def parse(*args):
            nonlocal specs
            parser = PosArgsCollectorAndBinder(specs)
            with CommandLine(['$PROGRAM']+list(args)) as tokens:                
                posargs = parser.parse(tokens)
            n = len(list(tokens))
            return posargs,n
        return parse

    parse = create_new_parse(posargs_spec_1)

    assert parse('a1','a2','0.3','0.4') == ( {'l1': 'a1', 'l2': 'a2', 't3': 0.3, 't4': 0.4, 'v': []},0 )

    with pytest.raises(CommandLine.ErrorInContext) as info:
        parse('a1','a2','0.3')

    assert str(info.value) == textwrap.dedent("""

    $PROGRAM: CommandLine.ErrorInContext:
        $PROGRAM a1 a2 0.3    
                           ---
        not enough arguments."""
    )

    # TODO: More systematic tests (233a660d-c7c2-42f3-9dd3-4b6725fe1e53)
    # (copy from older sk_combinators?)

# **   Delimiters

from ..parsers import OptionalSeparator, optional_separator, EndOfArgs, end_of_args, Nothing, nothing

# **   Subcommands

from ..parsers import SubcommandsSwitch, SubcommandsParser


def test_spike_subcommands_switch():

    cmd0 = Struct( name = None, aliases = []
                   
    )
    cmd1 = Struct( name = 'foo', aliases = ['f','FOO'] )
    cmd2 = Struct( name = 'bar', aliases = ['b'] )
    
    specs = [ cmd0, cmd1, cmd2 ]
    
    def parse(*args):
        nonlocal specs
        parser = SubcommandsSwitch(specs)
        with CommandLine(['$PROGRAM']+list(args)) as tokens:                
            subcommands = parser.parse(tokens)
        n = len(list(tokens))
        return subcommands,n

    assert parse('foo','baal') == (cmd1,1)
    assert parse('bar','baal') == (cmd2,1)

    assert parse('foo') == (cmd1,0)
    assert parse('bar') == (cmd2,0)

    assert parse() == (cmd0,0)
    assert parse('--') == (cmd0,1)
    
    
def test_spike_subcommands_parser():
    
    cmd0 = Struct( name = None, aliases = [], parser = nothing )

    cmd1 = Struct( name = 'foo', aliases = ['f','FOO'],
                   parser = OptionsAndPosArgsParser([
                       Struct( name='force', aliases = ['f'], key="force",  implied_value=True, convert = flag ),
                       Struct( name='alpha', aliases = ['a'], key="alpha",  convert = float )
                   ])
    )

    cmd2 = Struct( name = 'bar', aliases = ['b'],
                   parser = OptionsAndPosArgsParser([
                       Struct( name='beta', aliases = ['b'], key="beta", convert = int ),
                   ])
    )

    specs = [ cmd0, cmd1, cmd2 ]
    
    def parse(*args):
        nonlocal specs
        parser = SubcommandsParser(specs)
        with CommandLine(['$PROGRAM']+list(args)) as tokens:                
            results = parser.parse(tokens)
        n = len(list(tokens))
        return results + (n,)

    print( parse('foo','-f','a','b') )
    print( parse('bar','a','b') )
    print( parse('bar','-b','2') )

    # TODO: Convert in proper tests (c3d95fa0-3835-4c42-8c6a-904cf097578d)

    with raises(UserError,match="cannot convert option argument"):
        parse('bar','-b','NONUM')
    
# *   Combinators  ---------------------------------------------------------------|
# **   Sequence

from ..parsers import Sequence

def test_sequence_spike():

    def convert(options,posargs1,__separator__,posargs2,__end__):
        return options,[parg.lexeme for parg in posargs1],[parg.lexeme for parg in posargs2]
    
    parser = Sequence( OptionsParser(options_spec_1),
                       posargs_collector,
                       optional_separator,
                       posargs_collector,
                       end_of_args,
                       convert = convert
    )
    
    def parse(*args):
        with CommandLine(args,start=0) as tokens:
            result = parser.parse(tokens)        
            n = len(list(tokens))
        return result+(n,)


    assert parse('-f','a','b','--','x','y') == ({'force': True}, ['a', 'b'], ['x', 'y'],0)
    assert parse('-f','a','b') == ({'force': True}, ['a','b'], [],0)

    with pytest.raises(CommandLine.ErrorInContext) as info:
        parse('-f','a','b','--','x','y','-x')

    assert str(info.value) == textwrap.dedent("""

    -f: CommandLine.ErrorInContext:
        -f a b -- x y -x
                      --
        expected end of arguments here."""
    )


# *   Prefab combined parsers ----------------------------------------------------|
# **   Options, Then PosArgs

from ..parsers import OptionsThenPosArgsParser


def test_OptionsThenPosArgsParser_spike():

    def convert(options,pargs):
        return options,[parg.lexeme for parg in pargs]
    
    parser = OptionsThenPosArgsParser(options_spec_1,convert=convert)


    def parse(*args):
        with CommandLine(args,start=0) as tokens:
            result = parser.parse(tokens)        
            n = len(list(tokens))
        return result+(n,)

    assert parse('-f','a','b') == ({'force': True},['a','b'],0)

    # TODO: cont/ with more tests here (62c79b18-bd13-4f74-803f-d472f3574420)
