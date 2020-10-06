# FileSystem for CSCI262 S4 2020
# Developed and tested in 3.8.5, Windows 10 Pro Version 2004
# Written by Jon K, 2020

import argparse


def is_init_mode():
    parser = argparse.ArgumentParser("FileSystem")
    parser.add_argument("-i", dest='init', action='store_true')
    args = parser.parse_args()
    return args.init

print(is_init_mode())
