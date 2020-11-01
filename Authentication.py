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
    
    def authenticate(self):
        user_id, user_data = UserDAO().get_user(self.__user.id)
        if user_id != None:
            user = User(user_id, user_data[0], user_data[1])
            hash_pass = sha256(self.__user.password.encode('utf-8')).hexdigest()
            
            if self.__user.name == user.name and hash_pass == user.password: 
                print("User {0} has logged successfully.".format(self.__user.name))
                return True
            else: 
                print("Name and/or password are incorrect. Permission denied.")
                return False
        
        return False