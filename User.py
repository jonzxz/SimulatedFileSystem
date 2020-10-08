class User:
    def __init__(self):
        self.__user_name = None
        self.__password_hash = None
        self.__clearance = None
        self.__salt = None

    def __init__(self, user_name, password_hash, salt, clearance):
        self.__user_name = user_name
        self.__password_hash = password_hash
        self.__salt = salt
        self.__clearance = clearance

    def get_user_name(self):
        return self.__user_name

    def get_password_hash(self):
        return self.__password_hash

    def get_salt(self):
        return self.__salt

    def get_clearance(self):
        return self.__clearance

    def __str__(self):
        return ("\nUsername: {}\nHash: {}\nClearance: {}\n"
        .format(self.__user_name, self.__password_hash, self.__clearance))

    def shadow_details(self):
        return "{}:{}:{}".format(self.__user_name, self.__password_hash, self.__clearance)

    def salt_details(self):
        return "{}:{}".format(self.__user_name, self.__salt)
