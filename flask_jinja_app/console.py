from cmd import Cmd
import main
import shlex
from website.models import Landlord, Tenant, House, Apartment

classes_str = ["Landlord", "Tenant", "House", "Apartment"]
classes = [Landlord, Tenant, House, Apartment]


class KejaFlaskShell(Cmd):
    intro = "Welcome to the Keja_Flask Shell. Type help or ? to get started!\n"
    prompt = '(Keja-Flask)> '

    def do_exit(self, inp):
        """Usage: Type exit or use shorthand Ctrl + D to exit."""
        print("Bye")
        return True

    def do_all(self, inp):
        obj_list = []
        inp_list = None
        if inp:
            inp_list = shlex.split(inp)

            if len(inp_list) > 1:
                print(
                    "Error can only take one class argument. Please try again with on class. Eg. <all Tenant>")
                return

            if inp_list[0] not in classes_str:
                print("Error class doesn't exist")
                return

            obj_list = inp_list[0].query.all()
        else:
            for cls_obj in classes:
                obj_list += cls_obj.query.all()

        print(obj_list)

    def do_create(self, inp):
        inp_list
        if inp:
            inp_list = shlex.split(inp)

    def do_delete(self, inp):
        pass

    def do_update(self, inp):
        pass

    do_EOF = do_exit


if __name__ == "__main__":
    KejaFlaskShell().cmdloop()
