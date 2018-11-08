import zaj4.validator as validator


def add_user_to_db(username, password, salt):
    if not validator.validate_username(username):
        with open('user_data.txt', 'a') as f:
            f.write(username + ' ' + password + ' ' + salt + '\n')
        return True
    else:
        return False