class File:
    def __init__(self):
        self.__file_name = None
        self.__owner = None
        self.__clearance = None

    def __init__(self, file_name, owner, clearance):
        self.__file_name = file_name
        self.__owner = owner
        self.__clearance = clearance

    def get_file_name(self):
        return self.__file_name

    def get_owner(self):
        return self.__owner

    def get_clearance(self):
        return self.__clearance

    def __str__(self):
        return "File Name: {}\nOwner: {}\nClearance: {}".format(self.__file_name, self.__owner, self.__clearance)
