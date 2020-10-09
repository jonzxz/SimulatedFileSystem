import os
from File import File

def read_file_data(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except FileNotFoundError as fnfe:
        Path(file_name).touch()

# Adds a line break if file is not empty otherwise appended data starts on same line
def write_to_file(file_name, data, mode):
    with open (file_name, mode) as file:
        if not os.stat(file_name).st_size == 0:
            file.write("\n")
        file.write(data)
    file.close()

# Function to test for presence of file in file list by name
def is_file_exist(file_entered, filelist):
    return file_entered in [file.get_file_name() for file in filelist]

# Function to return list of File
# Creates File objects on runtime
def get_files_in_store():
    file_list = []
    if os.path.exists('files.store'):
        with open ('files.store') as file_store:
            data = [file.strip() for file in file_store.readlines()]
        for file in data:
            file_details = file.split(sep=":")
            file_list.append(File(file_details[0], file_details[1], file_details[2]))
    return file_list

def update_file_store_records():
    if os.path.exists('files.store.tmp'):
        with open ('files.store.tmp', 'r') as fs_temp:
            fs_temp_data = fs_temp.read()
        fs_temp.close()
        write_to_file('files.store', fs_temp_data, 'a')
        os.remove('files.store.tmp')

def update_file_store_buffer(file_name, usrname, clearance):
    to_tmp_fs_buff = "{}:{}:{}".format(file_name, usrname, clearance)
    write_to_file('files.store.tmp', to_tmp_fs_buff, 'a')
    # with open ('files.store.tmp', 'a') as file_store:
    #     file_store.write("{}:{}:{}".format(file_name, usrname, clearance))

# Function to write to salt.txt
def write_to_salt(data):
    write_to_file('salt.txt', data, 'a')

# Function to write to shadow.txt
def write_to_shadow(data):
    write_to_file('shadow.txt', data, 'a')
