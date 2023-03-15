from cmd import Cmd
from website import create_app
import shlex
from website.models import Landlord, Tenant, House, Apartment

app = create_app()
classes_str = ["landlord", "tenant", "house", "apartment"]
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
                    "Error: <all> can only take one class argument. Please try again. Eg. <all Tenant>")
                return

            if inp_list[0].lower() not in classes_str:
                print("Error: Class doesn't exist")
                return

            index = classes_str.index(inp_list[0].lower())
            with app.app_context():
                obj_list = classes[index].query.all()
        else:
            with app.app_context():
                for cls_obj in classes:
                    obj_list += cls_obj.query.all()

        print(obj_list)

    def do_create(self, inp):
        obj_dict = {}
        if not inp:
            print("Error: Class name missing!")
            return

        args = shlex.split(inp)
        cls_str = args.pop(0)

        if cls_str.lower() not in classes_str:
            print("Error! Class doesn't exist!")

        for arg in args:
            if "=" not in arg:
                print("Error: Key not assigned. E.g <'id=234579'>")
                return
            arg = arg.replace(" ", "")
            print(arg)
            split_arg = arg.split("=")
            obj_dict[split_arg[0]] = split_arg[1]

        print(obj_dict)

    def do_delete(self, inp):
        pass

    def do_update(self, inp):
        pass

    do_EOF = do_exit


if __name__ == "__main__":
    KejaFlaskShell().cmdloop()
