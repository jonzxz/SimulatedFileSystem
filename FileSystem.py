# FileSystem for CSCI262 S4 2020
# Developed and tested in 3.8.5, Windows 10 Pro Version 2004
# Written by Jon K, 2020

from argparse import ArgumentParser
from sys import exit
from random import randint
from getpass import getpass
from User import User
from FileUtils import write_to_salt, write_to_shadow
from UserUtils import login, process_user_choice, menu_select
from UserUtils import check_pwd, check_existing_user, make_md5_hash
from CustomExceptions import PasswordComplexityException, UserAlreadyExistException

def main():
    if is_init_mode():
        init_mode()
    else:
        # returns User / False. if false then the failure will be caught in login
        user_logged_in = login()
        if user_logged_in:
            # pass in user name and user choice
            while True:
                user_choice = menu_select()
                process_user_choice(user_logged_in.get_user_name(),
                user_logged_in.get_clearance(), user_choice)

## Utilities
def is_init_mode():
    parser = ArgumentParser("FileSystem")
    parser.add_argument("-i", dest='init', action='store_true')
    args = parser.parse_args()
    return args.init

## User Creation
def init_mode():
    print("User Creation",
    "\n==============")
    # Entered password values will not be shown
    username = input("Username: ")
    pwd = getpass()
    cfm_pwd = getpass("Confirm Password: ")
    user_clearance = None
   #username = "jon"

    try:
        # insert user existence check here
        if check_existing_user(username):
            raise UserAlreadyExistException("User already exist, please choose another username\n")

    #pwd = "12345678!aB"
    #cfm_pwd = "12345678!aB"
        if check_pwd(pwd, cfm_pwd):
            is_clearance_valid = False
            while not is_clearance_valid:
                user_clearance = input("User clearance(0 - 3): ")
                #user_clearance = 3
                if int(user_clearance) <= 3: is_clearance_valid = True
                else: print("Invalid value, please enter only values from 0 to 3")

    except PasswordComplexityException as pce:
        print(pce)
        init_mode()
    except UserAlreadyExistException as uaee:
        print(uaee)
        init_mode()

    # Generate salt and write username:salt to salt.txt
    salt = make_salt()
    hashed_pwd_salt = make_md5_hash("{}{}".format(pwd, salt))

    # Creates a User instance
    user_created = User(username, hashed_pwd_salt, salt, user_clearance)
    write_to_salt(user_created.salt_details())

    # Generate MD5 hash of pwd|salt and write username:hash:usr_clr to shadow.txt
    write_to_shadow(user_created.shadow_details())
    print("Account {} successfully created, please restart program to login"
    .format(user_created.get_user_name()))

# Function to create a 8 digit long number
def make_salt():
    return ''.join(["{}".format(randint(0, 9)) for num in range (0, 8)])


main()
