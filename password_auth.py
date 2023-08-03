import hashlib
from config import auth_list, auth_details

def register(user_name, password, first_name, last_name, email):
    hash_pwd = hashlib.md5(password.encode()).hexdigest()
    fl = open(auth_list, "a+")
    fl.write(user_name + "\t" + str(hash_pwd) + "\n")
    fl.close()
    write_details(user_name, first_name, last_name, email)
    return [True, "Success!!"]

def write_details(user_name, first_name, last_name, email):
    fl = open(auth_details, "a+")
    fl.write(user_name + "\t" + first_name + "\t" + last_name + "\t" + email + "\n")
    fl.close()
    return [True, "Success!!"]
def logon(user_name, password):
    hash_pwd = hashlib.md5(password.encode()).hexdigest()
    user_found = False
    with open(auth_list) as f:
        for line in f:
            if line.split("\t")[0] == user_name:
                user_found = True
                if line.split("\t")[1].strip() != str(hash_pwd):
                    return False, 'Invalid Login Credentials!!'
        if not user_found:
            return False, 'Invalid Login Credentials!! Kindly Register!'
    return True, "Success!!"
