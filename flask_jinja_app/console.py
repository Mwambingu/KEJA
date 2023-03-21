from cmd import Cmd
from website import create_app
import shlex
from website.models import Landlord, Tenant, House, Apartment
from website import db

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
        """
        List all objects in the db or all of a specified class.

        Usage: List all objects <all>
        List all of a specified type <all Tenant>
        """
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
        Creates objects and saves to db.
        Usage: create Landlord first_name='Ligma'

        Required and allowed key word args:
        Landlord id, first_name, last_name, email, password
        House id, house_name, landlord_id
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
        """
        Deletes specified objects in the db.

        Usage: Delete all models. <delete all>
        Delete all of a specific type. <delete all Tenant>
        Delete a specific object. <delete Tenant id=1111>
        """
        delete_all_class = False
        if not inp:
            print(
                "Error: No argument given please try again. Run <help delete> for more information.")
            return

        input_args = shlex.split(inp)

        if len(input_args) > 2:
            print("Error: Argument threshold reached. Delete supports only 2 arguments.")
            return

        if input_args[0].lower() == "all":
            if len(input_args) == 1:
                with app.app_context():
                    db.drop_all()
                    db.create_all()
                    db.session.commit()
                    return
            else:
                delete_all_class = True

        if delete_all_class:
            if input_args[1].lower() not in classes_str:
                print("Error: Class doesn't exist")
                return

            cls_index = classes_str.index(input_args[1].lower())
            cls_to_delete = classes[cls_index]

            with app.app_context():
                cls_to_delete.query.delete()
                db.session.commit()

        if len(input_args) < 2:
            print("Error: Class argument missing!!")
            return

        cls_arg = input_args[1].split("=")[0]
        cls_id = input_args[1].split("=")[1]

        if cls_arg.lower() != "id":
            print("Error: id class argument missing. <Tenant id=1111>")
            return

        cls_index = classes_str.index(input_args[0].lower())
        cls_to_delete = classes[cls_index]

        with app.app_context():
            cls_obj = cls_to_delete.query.filter_by(id=cls_id.lower()).first()
            if cls_obj:
                db.session.delete(cls_obj)
                db.session.commit()
                return
            print("Error: {} class with id: {} doesn't exist!".format(
                str(cls_to_delete), cls_id))

    def do_update(self, inp):
        """
        Updates objects in the db. Strictly requires the class, id
        and at least 1 argument to update

        Usage: update Landlord id='1111' first_name='Ligma'

        Required and allowed key word args:
        Landlord id, first_name, last_name, email, password
        House id, house_name, landlord_id
        Apartment id, apt_no, room_type, rent, house_id
        Tenant id, first_name, last_name, tenant_id, apt_id, landlord_id
        """
        new_cls_obj = {}

        if not inp:
            print("Error: Class is missing!")
            return

        input_args = shlex.split(inp)
        cls_str = input_args.pop(0).lower()

        if cls_str not in classes_str:
            print("Error: Class doesn't exist")
            return

        cls_index = classes_str.index(cls_str)
        cls_to_update = classes[cls_index]

        if len(input_args) < 1:
            print("Error: Missing id argument!")
            return

        if len(input_args) < 2:
            print("Error: Missing argument to update!")
            return

        id_arg = input_args.pop(0)
        if "=" not in id_arg:
            print("Error: id is empty. Not assigned!")
            return
        check_id_arg = id_arg.split("=")[0]
        cls_id = id_arg.split("=")[1]

        if check_id_arg != "id":
            print("Error: Incorrect id argument! <id='1111'>")
            return

        with app.app_context():
            db_cls_obj = cls_to_update.query.filter_by(id=cls_id).first()
            if not db_cls_obj:
                print("Error: {} class with id {} doesn't exist.".format(
                    cls_str, cls_id))
                return

        for args in input_args:
            if "=" not in args:
                print("Error: Argument has not been assigned. <first_name=solo>")
                return
            key = args.split("=")[0]
            value = args.split("=")[1]

            if key not in model_args:
                print("Error: Key argument given is not supported.")
                return

            new_cls_obj[key] = value
            print(new_cls_obj)

        with app.app_context():
            db_cls_obj.update_obj(new_cls_obj)

    do_EOF = do_exit


if __name__ == "__main__":
    KejaFlaskShell().cmdloop()
