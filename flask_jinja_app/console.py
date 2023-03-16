from cmd import Cmd
from website import create_app
import shlex
from website.models import Landlord, Tenant, House, Apartment

app = create_app()
classes_str = ["landlord", "tenant", "house", "apartment"]
classes = [Landlord, Tenant, House, Apartment]
model_args = [
    "id",
    "first_name",
    "last_name",
    "email",
    "password",
    "house_name",
    "landlord_id",
    "apt_no",
    "room_type",
    "rent",
    "house_id",
    "tenant_id",
    "apt_id"]


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
        """
        Usage: create Landlord first_name="Ligma"

        Required and allowed key word args:
        Landlord id, first_name, last_name, email, password
        House id, house_name, landlord_id, no_of_apts
        Apartment id, apt_no, room_type, rent, house_id
        Tenant id, first_name, last_name, tenant_id, apt_id, landlord_id
        """
        obj_dict = {}
        if not inp:
            print("Error: Class name missing!")
            return

        args = shlex.split(inp)
        cls_str = args.pop(0).lower()

        if cls_str.lower() not in classes_str:
            print("Error! Class doesn't exist!")

        if cls_str.lower() == "apartment" or cls_str.lower() == "landlord":
            if len(args) != 5:
                print("Error: {} strictly requires 5 key args".format(
                    cls_str.lower()))
                return

        if cls_str.lower() == "tenant":
            if len(args) != 7:
                print("Error: {} strictly requires 7 key args".format(
                    cls_str.lower()))
                return

        if cls_str.lower() == "house":
            if len(args) != 3:
                print(
                    "Error: {} strictly requires 3 key args".format(
                        cls_str.lower))
                return

        for arg in args:
            if "=" not in arg:
                print("Error: Key not assigned. E.g <'id=234579'>")
                return
            arg = arg.replace(" ", "")
            split_arg = arg.split("=")
            if split_arg[0] not in model_args:
                print(
                    "Error: Key argument parsed is not allowed! Type <help create> to get a list of allowed key arguments per model")
                return
            obj_dict[split_arg[0]] = split_arg[1]

        cls_index = classes_str.index(cls_str.lower())
        cls_to_create = classes[cls_index]

        new_obj = cls_to_create(**obj_dict)

        print(new_obj.__dict__)
        with app.app_context():
            new_obj.save()

    def do_delete(self, inp):
        pass

    def do_update(self, inp):
        pass

    do_EOF = do_exit


if __name__ == "__main__":
    KejaFlaskShell().cmdloop()
