# FileSystem for CSCI262 S4 2020
# Developed and tested in 3.8.5, Windows 10 Pro Version 2004
# Written by Jon K, 2020

from argparse import ArgumentParser
from sys import exit
from random import randint
from getpass import getpass
from hashlib import md5



def is_init_mode():
    parser = ArgumentParser("FileSystem")
    parser.add_argument("-i", dest='init', action='store_true')
    args = parser.parse_args()
    return args.init


def main():
    if is_init_mode:
        init_mode()
    else:
        print("run prog")

def init_mode():
    print("User Creation",
    "\n==============")
#    username = input("Username: ")
    # Entered password values will not be shown
#    pwd = getpass()
#    cfm_pwd = getpass("Confirm Password: ")
    username = "jon"

    # insert user existence check here
    if check_existing_user(username):
        print("User {} already exist. Please choose another username".format(username))
        exit()

    pwd = "12345678!aB"
    cfm_pwd = "12345678!aB"
    if check_pwd(pwd, cfm_pwd):
        is_clearance_valid = False
        while not is_clearance_valid:
            #user_clearance = input("User clearance(0 - 3): ")
            user_clearance = 3
            try:
                if int(user_clearance) <= 3: is_clearance_valid = True
                else: raise ValueError("Invalid value, please enter only values from 0 to 3")
            except ValueError as ve:
                print(ve)

        # Generate salt and write username:salt to salt.txt
        salt = make_salt()
        #write_to_salt("{}:{}\n".format(username, salt))

        # Generate MD5 hash of pwd|salt and write username:hash:usr_clr to shadow.txt
        hashed_pwd_salt = make_md5_hash("{}{}".format(pwd, salt))
        #write_to_shadow("{}:{}:{}".format(username, hashed_pwd_salt, user_clearance))
        print("Account {} successfully created, please restart program to login".format(username))

# Function to display info when existing user is found
# parameter data[2] = [username, salt] from check_existing user
# def display_existing_user_details(data):
#     print("User {} found in salt.txt".format(data[0]))
#     print("Salt retrieved {}".format(data[1]))
#
#     with open('shadow.txt', 'r') as shadow_file:
#         credentials = [line.strip() for line in shadow_file.readlines()]
#     print(credentials)
#     for credential in credentials:
#         if data[0] == credential.split(sep=":")[0]:
#             print(data[0])


# Function to test if entered username is present
# return [user, salt] if present otherwise return None
def check_existing_user(username):
    with open('salt.txt', 'r') as salt_file:
        users = [line.strip() for line in salt_file.readlines()]
    try:
        return ([user.split(sep=":") for user in users
        if username == (user.split(sep=":")[0])][0])
    except IndexError:
        return None

# Returns MD5 hash of encoded parameter
def make_md5_hash(data):
    md5_instance = md5()
    md5_instance.update(data.encode())
    return md5_instance.hexdigest()

# Function to write to salt.txt
def write_to_salt(data):
    with open ('salt.txt', 'a') as salt_file:
        salt_file.write(data)
    salt_file.close()

# Function to write to shadow.txt
def write_to_shadow(data):
    with open ('shadow.txt', 'a') as shadow_file:
        shadow_file.write(data)
    shadow_file.close()

# Function to create a 8 digit long number
def make_salt():
    return ''.join(["{}".format(randint(0, 9)) for num in range (0, 8)])

# Checks for password equality and password complexity requirements
# More than 8 characters, contains upper and lower case alphabets
# numbers and special characters
def check_pwd(pwd, cfm_pwd):
    try:
        if pwd == cfm_pwd and len(pwd) >= 8:
            contains_spec = False
            contains_small_alpha = False
            contains_big_alpha = False
            contains_num = False
            for char in pwd:
                if char == " ":
                    raise ValueError("No spaces allowed in password, sorry!")
                if not(char.isalpha() or char.isdigit()):
                    contains_spec = True
                if char.isupper():
                    contains_big_alpha = True
                if char.islower():
                    contains_small_alpha = True
                if char.isdigit():
                    contains_num = True
            # print("contains_spec ", contains_spec)
            # print("contains_small ", contains_small_alpha)
            # print("contains_big ", contains_big_alpha)
            # print("contains_num ", contains_num)
            return (contains_spec and contains_big_alpha and contains_small_alpha and contains_num)
        else:
            raise ValueError("Password must be equal, contain at least 8 characters,"
            " 1 upper and lower-cased character, 1 number and 1 special symbol")
    except ValueError as ve:
        print(ve)
        exit()


main()
