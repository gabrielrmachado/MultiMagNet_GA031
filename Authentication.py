from hashlib import sha256
from Data import UserDAO

class User:
    def __init__(self):
        self.__userDAO = UserDAO()
    
    def login(self, id):
        self.__user_id, self.__user_data = self.__userDAO.get_user(id)
        input_password = input('Type the password of user {0} to login: '.format(self.__user_data[0]))
        input_password_hash = sha256(input_password.encode('utf-8')).hexdigest()
        
        if input_password_hash == self.__user_data[1]:
            print("User {0} has logged successfully.".format(self.__user_data[0]))
        else: 
            raise PermissionError("Password invalid. Permission denied.")

    def get_priority_logged_user(self):
        return self.__user_data[2]

    def get_name_user(self):
        return self.__user_data[0]

# user = User()
# user.login(3)
# print(user.get_priority_logged_user())