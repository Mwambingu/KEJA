#!/usr/bin/env python3
from models import storage
from models.landlord import Landlord
from models.tenants import Tenant
from models.apartment import Apartment
from models.house import House

# Account Authentication
def landlord():
    """Initiates Landlord's Account authentication"""
    print("Landlord Login:")
    print("Type: 'exit' on any field to leave")
    email = str(input("Enter email: "))
    password = str(input("Enter password: "))
    if email == "exit" or password == "exit":
        main()

    if '@' not in email:
        print("Enter a valid email address!!")
        landlord()
    
    obj_item = landlord_check(email, password)
    if obj_item:
        landlord_cli(obj_item)
    print("User doesn't exist or password is incorrect!!")
    landlord()

def landlord_check(em, pwd):
    obj_list=storage.list_all("Landlord")
    for obj_item in obj_list:
        if obj_item.email == em and obj_item.password == pwd:
            return obj_item
    return None

def tenant():
    """Initiates Tenant's Account authentication"""
    print("Tenant Login:")
    print("Type: 'exit' on any field to leave")
    tenant_id = str(input("Enter Tenant ID: "))
    password = str(input("Enter Tenant Password: "))
    if tenant_id == "exit" or password == "exit":
        main()
    tenant_cli()
    main()

def signup():
    print("SignUp")
    print("Type: 'exit' on any field to leave")
    first_name = str(input("Enter First name: "))
    last_name  = str(input("Enter Last name: "))
    password = str(input("Enter password: "))
    email = str(input("Enter email: "))
    print("\n")

    if username == "exit" or password == "exit" or email == "exit":
        main()

    if '@' not in email:
        print("Enter a valid email address!!")
        signup()
    print("User successfully created!!")
    print(f"Welcome {username}!!")
    main()

def login():
    """Initiates the login process"""
    print("""
    Login:
    1. Landlord Login
    2. Tenant Login
    3. Exit
    """)

    value = str(input("Enter value: "))
    print("\n")

    if value == "1":
        landlord()
    if value == "2":
        tenant()
    if value == "3":
        main()
    
    print("Incorrect input!")
    login()
    
# Account Actions and Management
def get_info(obj_item):
    obj_dict = obj_item.__dict__
    key_list = ['_sa_instance_state', 'id', 'updated_at', 'created_at', 'password']
    for key in key_list:
        if key in obj_dict:
            del obj_dict[key]
    
    for k, v in obj_dict.items():
        print("{}: {}".format(k, v))
    return

# Landlord CLI Functionality
def landlord_cli(obj_item):
    print("""
    Welcome Back!!
    1. Landlord Information
    2. Add House
    3. Houses
    4. Exit
    """)

    value = input("Enter value: ")
    if value == "1":
        get_info(obj_item)
    if value == "2":
        create_house(obj_item)
    if value == "3":
        house(obj_item)
    if value == "4":
        main()
    
    landlord_cli(obj_item)

def create_house(obj_item):
    house_dict = {}
    house_dict['house_name'] = input("Enter House Name: ")
    house_dict['landlord_id'] = obj_item.id

    new_house = House(**house_dict)
    print("{} has been successfully created!!".format(new_house))
    new_house.save()
    print("{} saved to db!!".format(new_house))
    return

def house(obj_item):
    house_objs = obj_item.houses
    count = 1
    for house_obj in house_objs:
        print("{}.{}".format(count, house_obj.house_name))
        count +=1
    value = int(input("Enter Value: "))

    print("{} has been selected!!".format(house_objs[value].house_name))
    house_cli(house_objs[value])
    return

def house_cli(obj_item):
    print("""
    1. Create Apartment
    2. Apartments
    3. Exit
    """)
    value = input("Enter value: ")

    if value == "1":
        create_apartment(obj_item)
    return

def create_apartment(obj_item):
    aptmt_dict = {}
    not_int = False
    new_aptmt = None

    aptmt_dict['apartment_no'] = input("Enter Apartment No: ")
    aptmt_dict['room_type'] = input("Enter apartment type: ")
    
    try:
        aptmt_dict['rent'] = int(input("Rent Amount: "))
    except (TypeError, ValueError):
        print("Invalid input! Please enter a valid amount!!")
        not_int = True
    
    if not not_int:
            aptmt_dict['house_id'] = obj_item.id
            new_aptmt = Apartment(**aptmt_dict)
            print("{} has been successfully created!!".format(new_aptmt))
            print(new_aptmt.__dict__)
            new_aptmt.save()
    else:
        create_apartment(obj_item)

    house_cli(obj_item)

# Tenant CLI Functionality
def tenant_cli():
    print("""
    Welcome Back!!
    1. Tenancy Information
    2. Rent Amount
    3. Landlord Contact
    4. Exit
    """)
    value = input("Enter value: ")

    if value == "1":
        print("The Tenant")
    if value == "2":
        print("Rent!!")
    if value == "3":
        print("Landlord!!")
    if value == "4":
        main()
    tenant_cli()

# Main application function
def main():
    """Launches the main Application"""
    print("""
    Welcome to KeJa!
    Manage your houses your own way!
    Choose an option:
    1. Signup
    2. Login
    3. Exit
    """)

    value = str(input("Enter value: "))
    print("\n")

    if value == "1":
        signup()
    if value == "2":
        login()
    if value == "3":
        print("Thank you for using KEJA!")
        quit()
    print("Incorrect input!")
    main()

main()