#!/usr/bin/env python3

#                                       # begin-example

from greenland.cmdline.shellcommands import *

class Greet(ShellCommand):
    """
    Greet, (C) 2018, M E Leypold

    Usage: greet [-l] [-p $PHRASE] [$WHOM]

    Greet future minions of you, alien overlords.
    """

    usage = [
        Flag   ('leader', ['l'], "Ask for their leader"),
        Option ('phrase', ['p'], str, "Greeting phrase to use", default="Hello"),

        Optional ('whom',str,"whom to greet")
    ]

    def main(self,whom = 'people'):
        print(self.phrase+", "+whom+"!")
        if self.leader: print("Bring me to your leader!")

        
if __name__ == '__main__': Greet()

#                                       # end-example
