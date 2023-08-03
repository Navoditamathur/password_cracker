from password_auth import *
from password_cracker import crack_pwd

# PART-1

def isp_register():
    fname = input("First Name:").strip()
    lname = input("Last Name:").strip()
    email = input("Email:").strip()
    uname = input("Username:").strip().lower()
    pwd = input("Password:").strip().lower()
    status, msg = register(uname, pwd, fname, lname, email)
    print(msg)
    if not status:
        isp_register()

def isp_logon():
    uname = input("Username:").lower()
    pwd = input("Password:").strip()
    status, msg = logon(uname, pwd)
    print(msg)
    if not status:
        isp_logon()

# PART-2

def isp_crack_pwd():
    uname = input("Username:").strip().lower()
    response = crack_pwd(uname)
    if response[0]:
        msg = "Password cracked Successfully!!"
        password = response[1]
        time_taken = response[3]
        print(msg)
        print("password: "+password+"\nTime taken:"+str(time_taken))
    else:
        if len(response) == 5:
            msg = "Account not found with username " + uname + "!!"
        else:
            msg = "Unable to crack Password!!"
        print(msg)

# PART-3

def isp_validate_pwd():
    uname = input("Username:").strip()
    response = crack_pwd(uname)
    if response[0]:
        msg = "Password cracked Successfully!!"
        password = response[1]
        password_strength = response[2]
        print(msg+"\n")
        print("Password: "+password+"\nPassword strength: "+password_strength)
    else:
        if len(response) == 5 and len(response[4]) > 0:
            msg = "Account not found with username " + uname + "!!"
        else:
            msg = "Unable to crack Password!!"
        print(msg)


if __name__ == "__main__":
    c = True
    while c:
        print("Enter :\n 1. 1 to Register\n 2. 2 to login\n 3. 3 to crack password\n 4. 4 to validate password")
        choice = int(input("Your choice:"))
        if choice == 1:
            isp_register()
        elif choice == 2:
            isp_logon()
        elif choice == 3:
            isp_crack_pwd()
        else:
            isp_validate_pwd()
        cont = input("Do you want to continue?(Y/n):")
        if cont.lower() == "n":
            c = False
