#!/usr/bin/env python3
from cmd import Cmd
import shlex
from models import storage
from models.landlord import Landlord
from models.tenants import Tenant
from models.apartment import Apartment
from models.house import House

classes = ["Tenant", "House", "Landlord", "Apartment"]

class KejaShell(Cmd):
    intro = 'Welcome to KeJa Shell. Type help or ? to get started!\n'
    prompt = '(KeJa)> '
    
    def do_create(self, inp):
        """Usage: Creates objects
        ex: Create Tenant <first_name> <last_name> <apartment_id>
        """
        inps = shlex.split(inp)
        
        if inps[0] not in classes:
            print("class name doesn't exits")
        
        if inps[0] == "Tenant":
            if len(inps) != 4:
                print("Missing inputs! \nex: Create Tenant <first_name> <last_name> <apartment_id>")

        if inps[0] == "House":
            if len(inps) != 4:
                print("Missing inputs! \nex: Create House <house_name> <landlord_id> <number_of_apartments>")

        if inps[0] == "Apartment":
            if len(inps) != 5:
                print("Missing inputs! \nex: Create Apartment <apartment_no> <room_type> <rent> <house_id>")

        if inps[0] == "Landlord":
            if len(inps) != 5:
                print(
                "Missing inputs! \nex: Create Landlord <first_name> <last_name> <email> <password> <apartment_id>")

        if obj:
            obj.save()

    def do_exit(self, inp):
        print("Bye")
        return True

    def help_exit(self):
        print("Usage: Type exit or use shorthand Ctrl + D to exit.")
    
    do_EOF = do_exit
    help_EOF = help_exit

if __name__ == "__main__":
    KejaShell().cmdloop()
        
