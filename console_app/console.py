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
    
    def do_all(self, inp=None):
        """Usage: Returns list of all objs or a all of a specified type
        ex: all or all Tenant"""
        if inp and inp not in classes:
            print("Class does not exist")
            return
        
        all_objs = storage.list_all(inp)
        print(all_objs)
        return

    def do_create(self, inp=None):
        """Usage: Creates objects
        ex: Create Tenant <first_name=''> <last_name=''> <apartment_id=''>
        """
        if not inp:
            print("Missing class!!")
            return 
        
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
            if len(inps) < 3:
                print("Missing inputs! \nex: Create Tenant <first_name=''> <last_name=''> <landlord_id>='' <apartment_id=''>")
                return
            obj = Tenant(**obj_dict)

        if cls_str == "House":
            if len(inps) < 2:
                print("Missing inputs! \nex: Create House <house_name=''> <landlord_id=''> <number_of_apartments=0>")
                return
            obj = House(**obj_dict)

        if cls_str == "Apartment":
            if len(inps) < 4:
                print("Missing inputs! \nex: Create Apartment <apartment_no=''> <room_type=''> <rent> <house_id=''>")
                return
            obj = Apartment(**obj_dict)

        if cls_str == "Landlord":
            print("Found Landlord!!")
            if len(inps) < 4:
                print(
                "Missing inputs! \nex: Create Landlord <first_name> <last_name> <email> <password> <apartment_id>")
                return
            obj = Landlord(**obj_dict)


        if obj:
            print("Object created successfully!!")
            print(obj)
            print(obj.__dict__)
            storage.reload()
            obj.save()


    def do_update(self, inp=None):
        """Usage: Updates a specified object
        ex: Update Tenant <id=""> <first_name=""> <last_name="">
        """
        if not inp:
            print("Missing class!!")
            return
        
        inps = shlex.split(inp)
        cls_str = inps.pop(0)
        obj_dict = {}
        obj_list = []
        obj = None

        # Splitting inputs into dictionary
        for key_value in inps:
            key_item = key_value.split("=")[0]
            if key_value.split("=")[1].isdigit():
                value_item = int(key_value.split("=")[1])
            else:
                value_item = key_value.split("=")[1]
            obj_dict[key_item] = value_item

        if "id" not in obj_dict:
            print("Please enter id of object!!")
            return
        
        obj_list = storage.list_all(cls_str)
        for obj_item in obj_list:
            if obj_item.id == obj_dict["id"]:
                obj = obj_item

        if obj:
            del obj_dict["id"]
            obj.update(obj_dict)
        else:
            print("Object Not Found!!")

        return


    def do_delete(self, inp):
        """Usage: Deletes A model specified by it's ID
        ex: delete Tenant <id=''>"""
        inps = shlex.split(inp)
        
        if not inps:
            print("Missing class!!")
            return
        if len(inps) < 2:
            print("Please enter an id!")
            return

        cls_str = inps.pop(0)
        cls_id = inps.pop(0).split("=")[1]
        obj_list = []

        if cls_str not in classes:
            print("Class doesn't exist!")
            return
        
        obj_list = storage.list_all(cls_str)

        for obj_item in obj_list:
            if obj_item.id == cls_id:
                storage.delete(obj_item)
                storage.save()
                print("Object with id {} has been deleted successfully!".format(cls_id))
                return
        print("Object with id {} doesn't exist!".format(cls_id))
        return

    def do_exit(self, inp):
        print("Bye")
        return True

    def help_exit(self):
        print("Usage: Type exit or use shorthand Ctrl + D to exit.")
    
    do_EOF = do_exit
    help_EOF = help_exit

if __name__ == "__main__":
    KejaShell().cmdloop() 
