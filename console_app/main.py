#!/usr/bin/env python3
# Account Authentication
def landlord():
    """Initiates Landlord's Account authentication"""
    email = str(input("Enter email: "))
    password = str(input("Enter password: "))

    landlord_cli()
    main()

def tenant():
    """Initiates Tenant's Account authentication"""
    tenant_id = str(input("Enter Tenant ID: "))
    password = str(input("Enter Tenant Password: "))

    tenant_cli()
    main()

def signup():
    print("SignUp")
    username = str(input("Enter username: "))
    password = str(input("Enter password: "))
    email = str(input("Enter email: "))
    print("\n")

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
def landlord_cli():
    print("""
    Welcome Back!!
    1. Landlord Information
    2. Apartments
    3. Tenants
    4. Exit
    """)

    value = input("Enter value: ")
    if value == "1":
        print("The Landlord")
    if value == "2":
        print("Apartments")
    if value == "3":
        print("Tenants")
    if value == "4":
        login()
    
    landlord_cli()

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
        login()
        
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

# if __name__ == "__main___":
#     main()
main()