from hashlib import sha256
from Data import UserDAO

class User:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

class Authentication:
    def __init__(self, user):
        self.__user = user

    def __readUser(self):
        # checks in a file whether a given name is present.
        return User(1, "Gabriel", "123456")
    
    def authenticate(self):
        user = self.__readUser()
        hash_pass = sha256(self.__user.password).hexdigest()
        if hash_pass == user.password: return True
        else: return False

