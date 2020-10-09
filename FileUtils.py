import os
from File import File

# Function to return data of file passed in by name
# Creates empty file if file does not exist
def read_file_data(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except FileNotFoundError as fnfe:
        Path(file_name).touch()

# Function to write data to file passed in by name
# Mode of writing passed in can be 'a' or 'w'
def write_to_file(file_name, data, mode):
    with open (file_name, mode) as file:
        # Adds a line break if file is not empty otherwise appended data starts on same line
        if not os.stat(file_name).st_size == 0:
            file.write("\n")
        file.write(data)
    file.close()

# Function returning bool to test for presence of file in file list by name
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

# Function to write newly created files into file.store
# Newly created files (unsaved) are stored in a temp buffer
# that is then moved into file.store when (S)ave is invoked
# Deletes file.store.tmp after Save.
def update_file_store_records():
    if os.path.exists('files.store.tmp'):
        with open ('files.store.tmp', 'r') as fs_temp:
            fs_temp_data = fs_temp.read()
        fs_temp.close()
        # Converts string to list by \n and typecast to set to get unique elements
        # Converts back to list and then joined to string with \n
        # To avoid created but unsaved entries becoming duplicates in filestore
        fs_temp_data = '\n'.join(list(set(fs_temp_data.split(sep="\n"))))
        write_to_file('files.store', fs_temp_data, 'a')
        os.remove('files.store.tmp')

# Writes file data filename:usr:clearance into temp filestore buffer
def update_file_store_buffer(file_name, usrname, clearance):
    to_tmp_fs_buff = "{}:{}:{}".format(file_name, usrname, clearance)
    write_to_file('files.store.tmp', to_tmp_fs_buff, 'a')

# Function to write to salt.txt
def write_to_salt(data):
    write_to_file('salt.txt', data, 'a')

# Function to write to shadow.txt
def write_to_shadow(data):
    write_to_file('shadow.txt', data, 'a')
