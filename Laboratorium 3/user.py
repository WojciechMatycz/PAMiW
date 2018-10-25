import hashlib

class User:

    def __init__(self, details_tab):
        self.login = details_tab[0]
        self.password = hashlib.sha256(details_tab[1].encode()).hexdigest()

    def check_password(self, password):
        passhash = hashlib.sha256(password.encode()).hexdigest()
        return self.password == passhash

    def to_db_record(self):
        return self.login + " " + self.password

    def __str__(self):
        return self.login + '\n' + self.password
