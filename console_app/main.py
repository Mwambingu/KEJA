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
def user_check(form, login_id, pwd, user_type_str):
    obj_list=storage.list_all(user_type_str)
    if form == "login":
        if user_type_str == "Landlord":
            for obj_item in obj_list:
                if obj_item.email == login_id and obj_item.password == pwd:
                    return obj_item
        if user_type_str == "Tenant":
            for obj_item in obj_list:
                if obj_item.tenant_id == login_id and obj_item.password == pwd:
                    return obj_item
    
    if form == "signup":
        for obj_item in obj_list:
            if obj_item.email == login_id:
                return True
    return None

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
    storage.reload()
    obj_list=storage.list_all(sim_obj.__class__.__name__)
    for obj_item in obj_list:
        if obj_item.id == sim_obj.id:
            return obj_item

def update_value(obj_to_update, attr, value):
    setattr(obj_to_update, attr, value)
    obj_to_update.update()
    return obj_to_update

def return_related_objs(obj, obj_class, id_attr, landlord_id):
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
                if obj_item.landlord_id == landlord_id:
                    new_obj_list.append(obj_item)
    
    if new_obj_list:
        return new_obj_list
    return None
    

def delete_related_values(related_obj, related_value):
    update_value(related_obj, "related_value", None)
    related_obj.update()


# Account Authentication
# Signup Module
def signup():
    screen_clear()
    landlord_dict = {}
    print("SignUp")
    print("Type: 'exit' on any field to leave")
    first_name = str(input("Enter First name: "))
    if first_name == "exit":
        return
    last_name  = str(input("Enter Last name: "))
    if last_name == "exit":
        return
    if not first_name.isalpha() and not last_name.isalpha():
        print("Names should not contain digits!")
        sleep(1)
        signup()

    password = str(input("Enter password: "))
    if password == "exit":
        return
    if len(password) < 8:
        print("Password length is too short!")
        sleep(1)
        signup()

    email = str(input("Enter email: "))
    if email == "exit":
        main()
    if '@' not in email:
        print("Enter a valid email address!!")
        sleep(1)
        signup()
    
    user_exists = user_check("signup", email, None, "Landlord")

    if user_exists == True:
        print("Email already exists!! Use a different one!")
        sleep(1)
        signup()


    landlord_dict["first_name"] = first_name
    landlord_dict["last_name"] = last_name
    landlord_dict["password"] = password
    landlord_dict["email"] = email

    print(landlord_dict)

    new_landlord_obj = Landlord(**landlord_dict)
    new_landlord_obj.save()

    print("User successfully created!!")
    print(f"Welcome {first_name}!!")
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
        landlord_check()
    if value == "2":
        tenant_check()
    if value == "3":
        main()
    
    print("Incorrect input!")
    login()

#Account Authenticaiton -- Login Module
def landlord_check():
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
        sleep(2)
        landlord_check()
    
    obj_item = user_check("login", email, password, "Landlord")
    if obj_item:
        landlord_cli(obj_item)
    print("User doesn't exist or password is incorrect!!")
    sleep(1)
    landlord_check()

def tenant_check():
    """Initiates Tenant's Account authentication"""
    screen_clear()
    print("Tenant Login:")
    print("Type: 'exit' on any field to leave")
    tenant_id = str(input("Enter Tenant ID: "))
    password = str(input("Enter Tenant Password: "))
    if tenant_id == "exit" or password == "exit":
        main()
    
    obj_item = user_check("login", tenant_id, password, "Tenant")
    if obj_item:
        tenant_cli(obj_item)
    print("User doesn't exist or password is incorrect")
    sleep(1)
    tenant_check()

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
        
        sleep(2)
        landlord_cli(obj_item)
    except (AttributeError):
        screen_clear()
        print("Print Unmapped Instance Error! Reloading.....")
        sleep(2)
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
    house_objs = storage.list_all("House")
    ld_house_objs = []
    no_of_houses = []
    count = 1

    for house_obj in house_objs:
        if house_obj.landlord_id == obj_item.id:
            ld_house_objs.append(house_obj)
    
    if ld_house_objs:
        print("{}'s Houses".format(obj_item.first_name))
        print("To go back type 'exit' as value")

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

        print("{} has been selected!!".format(ld_house_objs[value].house_name))
        house_cli(ld_house_objs[value])
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
    sleep(2)
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
    sleep(2)
    
    return

def get_tenants(obj_item):
    screen_clear()
    db_tenant_objs = storage.list_all("Tenant")
    tenant_objs = []
    no_of_tenants = []
    count = 1

    if db_tenant_objs:
        for db_tenant_obj in db_tenant_objs:
            if db_tenant_obj.landlord_id == obj_item.id:
                tenant_objs.append(db_tenant_obj)
        
    
    if tenant_objs:
        print("{}'s Tenants".format(obj_item.first_name))
        print("To go back type 'exit' as value")

        for n_tenant in range(len(tenant_objs)):
            no_of_tenants.append(str(n_tenant+1))

        for tenant_obj in tenant_objs:
            print("{}  {}".format(count, tenant_obj.first_name, tenant_obj.last_name))
            count+=1
        value = input("Enter value: ")

        if value == "exit":
            return
        
        print(no_of_tenants)
        if value not in no_of_tenants:
            print("Incorrect input!!")
            sleep(2)
            return
        
        if tenant_objs:
            landlord_tenant_cli(tenant_objs[int(value)-1])
        sleep(2)
        return
    
    print("No Tenants Found!!")
    sleep(2)
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
        sleep(2)
        return
    else:
        print("House: Not Assigned")
        sleep(2)
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
    3. Remove Tenant
    4. Go Back
    5. Logout
    """)
    value = input("Enter value: ")

    if value not in ["1", "2", "3", "4", "5"]:
        print("Incorrect Input")
    if value == "1":
        add_tenant(aptmt_obj)
    if value == "2":
        adjust_rent(aptmt_obj)
    if value == "3":
        remove_tenant(aptmt_obj)
    if value == "4":
        return
    if value == "5":
        main()
    sleep(2)
    apartment_cli(aptmt_obj)

def add_tenant(aptmt_obj):
    screen_clear()
    no_of_tenants = []
    count = 1
    landlord_id = aptmt_obj.houses.landlord_id
    tenant_list = return_related_objs(aptmt_obj, "Tenant", "apartment_id", landlord_id)

    if tenant_list == None:
        print("There aren't any listed tenants yet!")
        sleep(1)
        return
    if type(tenant_list) != list:
        print("Apartment is already assigned to a tenant")
        sleep(1)
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

def remove_tenant(aptmt_obj):
    new_aptmt_obj = reload_obj(aptmt_obj)
    tenant_list = new_aptmt_obj.tenants
    
    if tenant_list:
        tenant = tenant_list[0]
        print("You wish to remove {} from apartment?".format(tenant.first_name))
        print("Type 'yes' to continue or 'no' to go back")
        value = input("Enter value: ")
        if value == "no":
            return
        if value == "yes":
            tenant.apartment_id = None
            tenant.update()
            print("Tenant successfully removed!")
            return
    print("No tenant found!!")
    return

# Tenant Account CLI Functionality
def tenant_cli(obj_item):
    screen_clear()
    print("Hi {}".format(obj_item.first_name))
    print("""
    Welcome Back!!
    1. Tenancy Information
    2. Landlord Contact
    3. Logout
    """)
    value = input("Enter value: ")

    if value == "1":
        get_tenant_info(obj_item)
    if value == "2":
        get_landlord_info(obj_item)
    if value == "3":
        main()
    tenant_cli(obj_item)

def get_tenant_info(obj_item):
    aptmt_obj = obj_item.apartments
    print("Name: {} {}".format(obj_item.first_name, obj_item.last_name))
    print("Tenant ID: {}".format(obj_item.tenant_id))
    if aptmt_obj:
        print("House: {}".format(aptmt_obj.houses.house_name))
        print("Apartment No: {} Type: {}".format(aptmt_obj.apartment_no, aptmt_obj.rent))
        print("Rent Amount: {}".format(aptmt_obj.rent))
    else:
        print("House: Not Assigned")
    
    sleep(3)
    return

def get_landlord_info(obj_item):
    landlord = obj_item.landlords
    print("Name: {} {}".format(landlord.first_name, landlord.last_name))
    print("email: {}".format(landlord.email))

    sleep(3)
    return

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