# FileSystem for CSCI262 S4 2020
# Developed and tested in 3.8.5, Windows 10 Pro Version 2004
# Written by Jon K, 2020

import argparse
import re
from getpass import getpass


def is_init_mode():
    parser = argparse.ArgumentParser("FileSystem")
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
    pwd = "12345678!aB"
    cfm_pwd = "12345678!aB"
    print(check_pwd(pwd, cfm_pwd))

# Checks for password equality and invokes complexity check
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
                    return False
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
            return False
    except ValueError as ve:
        print(ve)

# Checks for password complexity requirements
# More than 8 characters, contains upper and lower case alphabets
# numbers and special characters
def check_pwd_complexity(pwd):
    if len(pwd) < 8:
        return False



main()
