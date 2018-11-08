import os


def create_user_dir_if_not_exists(username):
    userpath = 'userDirs/' + username + '/'
    if not os.path.exists(userpath):
        os.makedirs(userpath)
    return


def get_user_file_list(user_path):
    return os.listdir(user_path)