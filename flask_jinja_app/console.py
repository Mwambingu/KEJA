from cmd import Cmd
import main
import shlex
from website.models import Landlord, Tenant, House, Apartment

classes = ["Landlord", "Tenant", "House", "Apartment"]


class KejaFlaskShell(Cmd):
    intro = "Welcome to the Keja_Flask Shell. Type help or ? to get started!\n"
    prompt = '(Keja-Flask)> '

    def do_exit(self, inp):
        """Usage: Type exit or use shorthand Ctrl + D to exit."""
        print("Bye")
        return True

    def do_all(self, inp):
        if inp:
            print(type(inp))
            print("Argument Found!")
        else:
            print("No Argument Found!")

    def do_create(self, inp):
        if inp:
            cmds = shlex.split(inp)
            if cmds[0] not in classes:
                print("Class does not exist")
            else:
                print(cmds)
        else:
            print("No commnad found!")

    def do_delete(self, inp):
        pass

    def do_update(self, inp):
        pass

    do_EOF = do_exit


if __name__ == "__main__":
    KejaFlaskShell().cmdloop()
