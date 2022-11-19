#!/usr/bin/env python3
from cmd import Cmd

class KejaShell(Cmd):
    intro = 'Welcome to KeJa Shell. Type help or ? to get started!\n'
    prompt = '(KeJa)> '

    def do_exit(self, inp):
        print("Bye")
        return True


    def help_exit(self):
        print("Usage: Type exit or use shorthand Ctrl + D to exit.")
    
    do_EOF = do_exit
    help_EOF = help_exit

if __name__ == "__main__":
    KejaShell().cmdloop()
        
