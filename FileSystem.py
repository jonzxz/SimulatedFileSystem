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
    pwd = "12345678!!aB"
    cfm_pwd = "12345678!!aB"
    (check_pwd(pwd, cfm_pwd))

def check_pwd(pwd, cfm_pwd):
    if pwd == cfm_pwd and check_pwd_complexity(pwd):
        print(check_pwd_complexity(pwd))
    else:
        return False

def check_pwd_complexity(pwd):
    if len(pwd) < 8:
        return False

    contains_spec = False
    contains_small_alpha = False
    contains_big_alpha = False
    contains_num = False

    for char in pwd:
        if char == " ":
            print("No spaces allowed in password, sorry!")
            return False
        if not char.isalpha() and not char.isdigit():
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

main()
