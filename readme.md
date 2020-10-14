# FileSystem
----
## Introduction
- This project is a simulated File System in UNIX-style written in Python
- Project access control level complies with the Bell-LaPadula (BLP) model

## Features
- Simple implementation of user registration and login
    - User creation are stored in salt.txt and shadow.txt to imitate salt and shadow in UNIX
        - `salt.txt` contains `username:random_salt`
        - `shadow.txt` contains `username:md5(password|salt):access_level`
- 4 Stages of access level from `0 to 4` for users
    - Higher value indicates higher authority
    - Access permissions are based off BLP
- Allows users to create, write, update and list files
    - Files are only considered "valid" if created and saved by the `FileSystem` process.
        - If files are not created using the program, it will not be recorded as all file presence records are stored in `files.store`

## Usage
- `git clone` the repository
- Execute the program with the `-i` flag to register yourself as a new user
    - `py -m FileSystem -i` or `python FileSystem.py -i`
        - `py3` is required instead of `py` if you have Python 2 and 3 installed
- Execute program with no flags to start the login process
    - `py -m FileSystem` or `python FileSystem.py`
        - `py3` is required instead of `py` if you have Python 2 and 3 installed

```
Developed and tested in Python 3.8.5, Windows 10 Pro Version 2004
Written by Jon K, 2020
```
