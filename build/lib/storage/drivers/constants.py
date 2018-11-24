class ErrorMessages:
    class Users:
        LOGIN_FAILED = 'Invalid username or password.'
        CANNOT_FIND_ROLE = 'Could not find role for the user.'
        INVALID_ROLE = 'Invalid role: "{}".'
        USER_IN_DATABASE = 'User with email "{}" is already in database.'
        NO_ACCESS = 'User with role "{}" does not have access to this.'
