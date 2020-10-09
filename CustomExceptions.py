# Custom exception classes for the sake of clearer handling
# instead of prints all over the place
class InsufficientPermissionsException(Exception):
    pass

class FileAlreadyExistException(Exception):
    pass

class FileNotInRecordException(Exception):
    pass

class AuthenticationFailureException(Exception):
    pass

class InvalidSelectionException(Exception):
    pass

class PasswordComplexityException(Exception):
    pass

class UserAlreadyExistException(Exception):
    pass
