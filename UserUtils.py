import os
from pathlib import Path
from getpass import getpass
from hashlib import md5
from User import User
from FileUtils import get_files_in_store, is_file_exist, read_file_data
from FileUtils import update_file_store_buffer, update_file_store_records, write_to_file
from CustomExceptions import InsufficientPermissionsException, FileAlreadyExistException
from CustomExceptions import FileNotInRecordException, AuthenticationFailureException
from CustomExceptions import InvalidSelectionException, PasswordComplexityException

def check_user_permissions(file_name, user_clearance, filelist):
    for file in filelist:
        if file.get_file_name() == file_name and file.get_clearance() <= user_clearance:
            return True
    return False

# Function to return [usrname, hash, clearance] from shadow if username
# exist in shadow
def read_shadow_for_user(username):
    with open('shadow.txt', 'r') as shadow_file:
        credentials = [line.strip() for line in shadow_file.readlines()]
    for credential in credentials:
        if username == credential.split(sep=":")[0]:
            return credential.split(sep=":")

# Function to display info when existing user is found
# parameter data[2] = [username, salt] from check_existing user
def get_user_details(usrname):
    try:
        data = check_existing_user(usrname)
        if not data:
            raise ValueError("\nUser does not exist")
        print("User {} found in salt.txt".format(data[0]))
        print("Salt retrieved from salt.txt: {}".format(data[1]))
        return data
    except ValueError as e:
        print(e)
        exit()

# Function to test if entered username is present
# return [user, salt] if present otherwise return None
def check_existing_user(username):
    try:
        if os.path.exists('salt.txt'):
            with open('salt.txt', 'r') as salt_file:
                users = [line.strip() for line in salt_file.readlines()]
            return ([user.split(sep=":") for user in users
            if username == (user.split(sep=":")[0])][0])
    except IndexError:
        return None

# Checks for password equality and password complexity requirements
# More than 8 characters, contains upper and lower case alphabets
# numbers and special characters
def check_pwd(pwd, cfm_pwd):
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
        if (contains_spec and contains_big_alpha
        and contains_small_alpha and contains_num):
            return True
        else:
            raise PasswordComplexityException("Password is not equal, or does not meet " \
            "complexity requirements.\nPassword must contain at least 8 characters, " \
            "upper and lower case characters,\nnumbers and special characters.\n")


# Authorisation / Authorised entity features
# Returns User / None based on authentication result
def login():
    try:
        entered_usrname = input("Username: ")
        entered_password = getpass()
        # entered_usrname = "jon"
        # entered_password = "12345678!aB"

        # Returns [0] = username
        #         [1] = salt from salt.txt
        user_salt_data = get_user_details(entered_usrname)
        # Returns [0] = username
        #         [1] = hashed_pwd_salt
        #         [2] = clearance
        user_shadow_data = read_shadow_for_user(entered_usrname)

        #print("Entered user: {}\nretrieved user(salt): {}\nretrieved user(shadow): {}".format(entered_usrname, user_salt_data[0], user_shadow_data[0]))
        #print("Entered password: {}".format(entered_password))
        #print("Retrieved salt: {}".format(user_salt_data[1]))
        #print("Retrieved hashed PW: {}".format(user_shadow_data[1]))
        print("Hashing...")
        print("Hash value: {}".format(make_md5_hash("{}{}"
        .format(entered_password, user_salt_data[1]))))

        # if shadow's md5(pwd|salt) == md5(entered_pwd|salt)
        if user_shadow_data[1] == make_md5_hash("{}{}"
        .format(entered_password, user_salt_data[1])):
            logged_in_user = User(user_shadow_data[0], user_shadow_data[1]
            , user_salt_data[1], user_shadow_data[2])
            print("\nAuthentication for user {0} complete.\nClearance for {0} is {1}"
            .format(logged_in_user.get_user_name(), logged_in_user.get_clearance()))
            return logged_in_user
        else:
            raise AuthenticationFailureException("Wrong username/password\n")
    except AuthenticationFailureException as afe:
        print(afe)
        login()

def menu_select():
    is_choice_valid = False
    valid_choices = ['C', 'A', 'R', 'W', 'L', 'S', 'E']

    print("\n(C)reate, (A)ppend, (R)ead, (W)rite, (L)ist, (S)ave, (E)xit: " , end="")
    choice = input().upper()
    if choice in valid_choices:
        return choice
    else:
        print("Invalid selection, please enter again!\n")

def process_user_choice(username, user_clearance, user_choice):
    files_present = get_files_in_store()
    try:
        if user_choice == 'C':
            file_name = input("Please enter file name to be created (with extensions): ")
            if is_file_exist(file_name, files_present):
                raise FileAlreadyExistException("File already exist, returning to main menu..")
            else:
                Path(file_name).touch()
                print("{} created, returning to menu...".format(file_name))
                update_file_store_buffer(file_name, username, user_clearance)

        elif user_choice == 'A':
            file_name = input("Please enter file name to open and append: ")
            if is_file_exist(file_name, files_present):
                if check_user_permissions(file_name, user_clearance, files_present):
                    user_data_to_append = input("Enter data to append to file: ")
                    write_to_file(file_name, user_data_to_append, 'a')
                    print("\nData appended to file {}, returning to menu..".format(file_name))
                else:
                    raise InsufficientPermissionsException("Insufficient permissions!")
            else:
                raise FileNotInRecordException("File not found in records, "\
                "if you have just created the file, save first")
        elif user_choice == 'R':
            file_name = input("please enter file name to read: ")
            if is_file_exist(file_name, files_present):
                if check_user_permissions(file_name, user_clearance, files_present):
                    print("Contents of file {}\n=============================="
                    .format(file_name))
                    print(read_file_data(file_name))
                    print("==============================\nEnd of file")
                else:
                    raise InsufficientPermissionsException("Insufficient permissions!")
            else:
                raise FileNotInRecordException("File not found in records, " \
                "if you have just created the file, save first")
        elif user_choice == 'W':
            file_name = input("Please enter file name to write: ")
            if is_file_exist(file_name, files_present):
                if check_user_permissions(file_name, user_clearance, files_present):
                    user_data_to_write = input("Enter data to write to file *ALL EXISTING DATA WILL BE LOST*: ")
                    write_to_file(file_name, user_data_to_write, 'w')
                    print("\nData written to file {}, returning to menu..".format(file_name))
                else:
                    raise InsufficientPermissionsException("Insufficient permissions!")
            else:
                raise FileNotInRecordException("File not found in records, " \
                "if you have just created the file, save first")
        elif user_choice == 'L':
            print("Files recorded in store\n=======================")
            if files_present:
                print("{}".format("\n".join([file.get_file_name() for file in files_present])))
            else:
                print("Records are empty - no files stored in records")
        elif user_choice == 'S':
            print("Saving all newly created files into record...")
            update_file_store_records()
        elif user_choice == 'E':
            is_choice_valid = False
            while not is_choice_valid:
                print("\nPlease remember to save before you quit!")
                shutdown = input("Shut down the file system? (Y)es or (N)o: ").upper()
                if shutdown == 'Y':
                    print("Exiting now, newly created files not saved will not be recorded into the store!")
                    exit()
                elif shutdown == 'N':
                    is_choice_valid = True
                else:
                    print("Invalid selection")
    except FileAlreadyExistException as faee:
        print(faee)

    except FileNotInRecordException as fnire:
        print(fnire)

    except InsufficientPermissionsException as ipe:
        print(ipe)

    except InvalidSelectionException as ise:
        print(ise)

# Returns MD5 hash of encoded parameter
def make_md5_hash(data):
    md5_instance = md5()
    md5_instance.update(data.encode())
    return md5_instance.hexdigest()
