import hashlib


def validate_user(user_details):
    username = user_details[0]
    hashed_passw = hashlib.sha256(user_details[1].encode()).hexdigest()
    users_data = open('user_data.txt', 'r')

    for user in users_data.readlines():
        user_data = user.split(' ')
        if username == user_data[0]:
            c = user_data[1][:-1]
            if hashed_passw == user_data[1][:-1]:
                return True
    return False


def validate_username(username):
    users_data = open('user_data.txt', 'r')

    for user in users_data.readlines():
        user_data = user.split(' ')
        if username == user_data[0]:
            return True

    return False