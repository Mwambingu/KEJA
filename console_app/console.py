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
        ex: Create Tenant <first_name=''> <last_name=''> <apartment_id=''>
        """
        inps = shlex.split(inp)
        cls_str = inps.pop(0)
        obj_dict = {}
        obj = None

        # Splitting inputs into dictionary
        for key_value in inps:
            key_item = key_value.split("=")[0]
            if key_value.split("=")[1].isdigit():
                value_item = int(key_value.split("=")[1])
            else:
                value_item = key_value.split("=")[1]
            obj_dict[key_item] = value_item
        
        print(obj_dict)

        
        if cls_str not in classes:
            print("class name doesn't exits")
            return
        
        if cls_str == "Tenant":
            if len(inps) != 3:
                print("Missing inputs! \nex: Create Tenant <first_name=''> <last_name=''> <apartment_id>=''")
                return
            obj = Tenant(obj_dict)

        if cls_str == "House":
            if len(inps) >= 2 and len(inps) < 4:
                print("Missing inputs! \nex: Create House <house_name=''> <landlord_id=''> <number_of_apartments=0>")
                return
            obj = House(obj_dict)

        if cls_str == "Apartment":
            if len(inps) != 4:
                print("Missing inputs! \nex: Create Apartment <apartment_no=''> <room_type=''> <rent> <house_id=''>")
                return
            obj = Apartment(obj_dict)

        if inps[0] == "Landlord":
            if len(inps) != 4:
                print(
                "Missing inputs! \nex: Create Landlord <first_name> <last_name> <email> <password> <apartment_id>")
                return
            obj = Landlord(obj_dict)


        if obj:
            print("Object created successfully!!")
            print(obj)


    def do_exit(self, inp):
        print("Bye")
        return True

    def help_exit(self):
        print("Usage: Type exit or use shorthand Ctrl + D to exit.")
    
    do_EOF = do_exit
    help_EOF = help_exit

if __name__ == "__main__":
    KejaShell().cmdloop() 
