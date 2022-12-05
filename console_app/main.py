#!/usr/bin/env python3
import os
import random
from models import storage
from models.landlord import Landlord
from models.tenants import Tenant
from models.apartment import Apartment
from models.house import House
from time import sleep


# Other Functions

def get_pass():
    letters_alpha = ["abcdefghijklmnopqrstuvwxyz", "abcdefghijklmnopqrstuvwxyz".upper(), "1234567890", "!@#$%"]
    choice = ""
    pass_size = []
    rand_size = 0
    pass_str = ""

    for i in range(8):
        pass_size = []
        rand_size = 0
        choice = random.choice(letters_alpha)
        size = len(choice)
        for i in range(size):
            pass_size.append(i)
        rand_size = random.choice(pass_size)
        pass_str += choice[rand_size]
    return pass_str

def screen_clear():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')

def reload_obj(sim_obj):
    obj_list=storage.list_all(sim_obj.__class__.__name__)
    for obj_item in obj_list:
        if obj_item.id == sim_obj.id:
            return obj_item

def reload_obj_list(obj_to_reload, item):
    obj_item = reload_obj(obj_to_reload)
    obj_item_list = getattr(obj_item, item)

    return obj_item_list

# Account Authentication
# Signup Module
def signup():
    screen_clear()
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
    sleep(2)
    main()

# Login Module
def login():
    """Initiates the login process"""
    screen_clear()
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

#Account Authenticaiton -- Login Module
def landlord():
    """Initiates Landlord's Account authentication"""
    screen_clear()
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
    sleep(1)
    landlord()

def landlord_check(em, pwd):
    obj_list=storage.list_all("Landlord")
    for obj_item in obj_list:
        if obj_item.email == em and obj_item.password == pwd:
            return obj_item
    return None

def tenant():
    """Initiates Tenant's Account authentication"""
    screen_clear()
    print("Tenant Login:")
    print("Type: 'exit' on any field to leave")
    tenant_id = str(input("Enter Tenant ID: "))
    password = str(input("Enter Tenant Password: "))
    if tenant_id == "exit" or password == "exit":
        main()
    tenant_cli()
    main()

# Landlord CLI Functionality
def landlord_cli(obj_item):
    try:
        screen_clear()
        print("""
        {} Welcome Back!!
        1. Landlord Information
        2. Add House
        3. Houses
        4. Tenants
        5. Logout
        """.format(obj_item.first_name))

        value = input("Enter value: ")
        if value == "1":
            print("Name: {} {}".format(obj_item.first_name, obj_item.last_name))
            print("Email: {}".format(obj_item.email))
        if value == "2":
            create_house(obj_item)
        if value == "3":
            get_houses(obj_item)
        if value == "4":
            access_tenants(obj_item)
        if value == "5":
            main()
        if value not in ["1", "2", "3", "4", "5"]:
            print("Incorrect Input!!")
            sleep(1)
        
        sleep(3)
        landlord_cli(obj_item)
    except (AttributeError):
        screen_clear()
        print("Print Unmapped Instance Error! Reloading.....")
        sleep(3)
        landlord_cli(obj_item)

# Creating houses and management cli
def create_house(obj_item):
    screen_clear()
    house_dict = {}
    house_dict['house_name'] = input("Enter House Name: ")
    house_dict['landlord_id'] = obj_item.id

    new_house = House(**house_dict)
    print("{} has been successfully created!!".format(new_house.house_name))
    new_house.save()
    print("{} saved to db!!".format(new_house.house_name))
    obj_item.update()
    return

def get_houses(obj_item):
    screen_clear()
    print("{}'s Houses".format(obj_item.first_name))
    print("To go back type 'exit' as value")
    house_objs = storage.list_all("House")
    ld_house_objs = []
    no_of_houses = []
    count = 1

    for house_obj in house_objs:
        if house_obj.landlord_id == obj_item.id:
            ld_house_objs.append(house_obj)
    
    if ld_house_objs:
        for n_house in range(len(ld_house_objs)):
            no_of_houses.append(str(n_house+1))

        for ld_house_obj in ld_house_objs:
            print("{}.{}".format(count, ld_house_obj.house_name))
            count +=1
        value = input("Enter Value: ")

        if value == "exit":
            landlord_cli(obj_item)
        
        if value not in no_of_houses:
            print("Incorrect Value!")
            sleep(1)
            return
        
        value = int(value)-1

        print("{} has been selected!!".format(house_objs[value].house_name))
        house_cli(house_objs[value])
        return
    print("No Houses Found!")
    sleep(2)
    return

# Creating Tenants accounts and management cli
def access_tenants(obj_item):
    screen_clear()
    cont = None
    print("""
    1. Create Tenant
    2. Tenants
    3. Go back
    """)
    value = input("Enter value: ")
    if value == "1":
        cont = create_tenants(obj_item)
    if value == "2":
        cont = get_tenants(obj_item)
    if value == "3":
        landlord_cli(obj_item)
    if value not in ["1", "2", "3"]:
        print("Incorrect Input!!")
        sleep(1)
        access_tenants(obj_item)
    sleep(3)
    access_tenants(obj_item)

def create_tenants(obj_item):
    screen_clear()
    obj_dict = {}
    random_int = random.randint(1000,9999)
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    password = get_pass()
    tenant_id = (first_name[:2] + last_name[:2] + str(random_int)).upper()

    obj_dict['first_name'] = first_name
    obj_dict['last_name'] = last_name
    obj_dict['password'] = password
    obj_dict['tenant_id'] = tenant_id
    obj_dict['landlord_id'] = obj_item.id

    new_tenant = Tenant(**obj_dict)
    new_tenant.save()

    print("{} successfully created!!".format(new_tenant))
    print("Tenant ID: {}".format(new_tenant.tenant_id))
    print("Password: {}".format(new_tenant.password))
    sleep(3)
    
    return

def get_tenants(obj_item):
    screen_clear()
    print("{}'s Tenants".format(obj_item.first_name))
    db_tenant_objs = storage.list_all("Tenant")
    tenant_objs = []
    no_of_tenants = []

    for db_tenant_obj in db_tenant_objs:
        if db_aptmt_obj.landlord_id == obj_item.id:
            tenant_objs.append(db_tenant_obj)
    for tenant_obj in tenant_objs:
        print("Tenant ID:{} | Name: {}  {} |".format(tenant_obj.tenant_id, tenant_obj.first_name, tenant_obj.last_name))
    sleep(3)
    return

# creating apartments and management cli
def house_cli(obj_item):
    screen_clear()
    print("{} Apartments: {}".format(obj_item.house_name, obj_item.number_of_apartments))
    print("""
    1. Create Apartment
    2. Apartments
    3. Go back
    4. Logout
    """)
    value = input("Enter value: ")

    if value == "1":
        create_apartment(obj_item)
    if value == "2":
        get_apartments(obj_item)
    if value == "3":
        landlord_cli(obj_item)
    if value == "4":
        main()
    if value not in ["1", "2", "3", "4"]:
        print("Incorrect Input!!")
        sleep(1)
        house_cli(obj_item)
    sleep(2)
    house_cli(obj_item)

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
            obj_item.number_of_apartments += 1
            obj_item.update()
            new_aptmt.save()
    else:
        create_apartment(obj_item)

    return

def get_apartments(obj_item):
    screen_clear()
    db_aptmt_objs = storage.list_all("Apartment")
    aptmt_objs = []

    for db_aptmt_obj in db_aptmt_objs:
        if db_aptmt_obj.house_id == obj_item.id:
            aptmt_objs.append(db_aptmt_obj)

    if aptmt_objs:
        print("{} Apartments".format(obj_item.house_name))
        print("To go back type 'exit' as value")
        no_of_aptmts = []
        count = 1
        for n in range(len(aptmt_objs)):
            no_of_aptmts.append(str(n+1))

        for aptmt_obj in aptmt_objs:
            apartment_no = aptmt_obj.apartment_no
            room_type = aptmt_obj.room_type
            rent = aptmt_obj.rent
            print("{}. Apartment No: {} Room Type: {} Rent: Ksh. {}".format(count, apartment_no, room_type, rent))
            count += 1

        value = input("Enter value: ")

        if value == "exit":
            house_cli(obj_item)

        if value not in no_of_aptmts:
            print("Incorrect Input!")
            get_apartments(obj_item)
        
        print("{} has been selected!!".format(aptmt_objs[int(value)-1].apartment_no))
        sleep(1)
        apartment_cli(aptmt_objs[int(value)-1], obj_item)
        return
    
    print("No Apartments Found!!")
    sleep(2)
    return

def apartment_cli(aptmt_obj, obj_item):
    screen_clear()
    print("""
    1. Add Tenant
    2. Adjust Rent
    3. Go back
    4. Logout
    """)
    value = input("Enter value: ")

    if value not in ["1", "2", "3", "4"]:
        print("Incorrect Input")
    if value == "1":
        print("Add Tenant coming soon...")
    if value == "2":
        print("Adjust Rent coming soon...")
    if value == "3":
        house_cli(obj_item)
    if value == "4":
        main()
    sleep(3)
    apartment_cli(aptmt_obj, obj_item)

# Tenant Account CLI Functionality
def tenant_cli():
    screen_clear()
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
    screen_clear()
    """Launches the main Application"""
    print("""
    Welcome to KeJa!
    Manage your houses your own way!
    Choose an option:
    1. Signup
    2. Login
    3. Exit
    """)

    value = input("Enter value: ")

    if value == "1":
        screen_clear()
        signup()
    if value == "2":
        screen_clear()
        login()
    if value == "3":
        print("Thank you for using KEJA!")
        sleep(2)
        quit()
        screen_clear()
    print("Incorrect input!")
    main()

main()