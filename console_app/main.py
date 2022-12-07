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

def update_value(obj_to_update, attr, value):
    setattr(obj_to_update, attr, value)
    obj_to_update.update()
    return obj_to_update

def return_related_objs(obj, obj_class, id_attr):
    obj_list = storage.list_all(obj_class)
    new_obj_list = []
    if not obj_list:
        return None
    for obj_item in obj_list:
        attr_value = getattr(obj_item, id_attr)
        if attr_value == obj.id:
            return obj_item
        else:
            if attr_value == None:
                new_obj_list.append(obj_item)
    return new_obj_list
    

def delete_related_values(related_obj, related_value):
    update_value(related_obj, "related_value", None)
    related_obj.update()


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
    print("""
    1. Create Tenant
    2. Tenants
    3. Go back
    """)
    value = input("Enter value: ")
    if value == "1":
        create_tenants(obj_item)
    if value == "2":
        get_tenants(obj_item)
    if value == "3":
        return
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
    print("To go back type 'exit' as value")
    db_tenant_objs = storage.list_all("Tenant")
    tenant_objs = []
    no_of_tenants = []
    count = 1

    if db_tenant_objs:
        for db_tenant_obj in db_tenant_objs:
            if db_tenant_obj.landlord_id == obj_item.id:
                tenant_objs.append(db_tenant_obj)
        
        for n_tenant in range(len(tenant_objs)):
            no_of_tenants.append(str(n_tenant+1))
    
    if tenant_objs:
        for tenant_obj in tenant_objs:
            print("{}  {}".format(count, tenant_obj.first_name, tenant_obj.last_name))
            count+=1
    
    value = input("Enter value: ")

    if value == "exit":
        return
    
    print(no_of_tenants)
    if value not in no_of_tenants:
        print("Incorrect input!!")
        sleep(3)
        return

    if not db_tenant_objs:
        print("No Tenants found!!")
        sleep(3)
        return
    
    if tenant_objs:
        landlord_tenant_cli(tenant_objs[int(value)-1])
    sleep(3)
    return

def landlord_tenant_cli(obj_item):
    screen_clear()
    aptmt_obj = obj_item.apartments

    print("{} {}".format(obj_item.first_name, obj_item.last_name))
    print("Tenant ID: {}".format(obj_item.tenant_id))
    if aptmt_obj:
        print("House: {}".format(aptmt_obj.houses.house_name))
        print("Apartment: {} | {}".format(aptmt_obj.apartment_no, aptmt_obj.room_type))
        print("Rent Amount: {}".format(aptmt_obj.rent))
    else:
        print("House: Not Assigned")
    
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
        return
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
            return

        if value not in no_of_aptmts:
            print("Incorrect Input!")
            return
        
        print("{} has been selected!!".format(aptmt_objs[int(value)-1].apartment_no))
        sleep(1)
        apartment_cli(aptmt_objs[int(value)-1])
        return
    
    print("No Apartments Found!!")
    sleep(2)
    return

def apartment_cli(aptmt_obj):
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
        add_tenant(aptmt_obj)
    if value == "2":
        adjust_rent(aptmt_obj)
    if value == "3":
        return
    if value == "4":
        main()
    sleep(3)
    apartment_cli(aptmt_obj)

def add_tenant(aptmt_obj):
    screen_clear()
    no_of_tenants = []
    count = 1
    tenant_list = return_related_objs(aptmt_obj, "Tenant", "apartment_id")

    if tenant_list == None:
        return
    if type(tenant_list) != list:
        print("Apartment is already assigned to a tenant")
        return
    
    print("List of tenants without apartments")
    print("Type go back type 'exit' as value")

    for n_tenants in range(len(tenant_list)):
        no_of_tenants.append(str(n_tenants+1))
    
    for tenant_obj in tenant_list:
        print("{}. {} {}".format(count, tenant_obj.first_name, tenant_obj.last_name))
        count+=1
    
    value = input("Enter value: ")

    if value == "exit":
        return

    if value not in no_of_tenants:
        print("Error incorrect input!")
        return
    
    tenant = tenant_list[int(value)-1]
    tenant = update_value(tenant, "apartment_id", aptmt_obj.id)
    print("{} {} has been assigned as new tenant.".format(tenant.first_name, tenant.last_name))
    return

def adjust_rent(aptmt_obj):
    print("Current rent amount: {}".format(aptmt_obj.rent))
    value = input("Enter new rent value: ")
    if not value.isdigit():
        print("Incorrect value!!")
        return

    aptmt_obj = update_value(aptmt_obj, "rent", value)
    print("Rent has been successfully updated to {}".format(aptmt_obj.rent))
    return



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