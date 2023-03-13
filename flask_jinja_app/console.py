from cmd import Cmd
import shlex
from website.models import Landlord, Tenant, House, Apartment

classes = ["Landlord", "Tenant", "House", "Apartment"]

class KejaFlaskShell(Cmd):
    intro = "Welcome to the Keja_Flask Shell. Type help or ? to get started!\n"
    prompt = '(Keja-Flask)>'

    def do_exit(self, inp):
        """Usage: Type exit or use shorthand Ctrl + D to exit."""
        print("Bye")
        return True