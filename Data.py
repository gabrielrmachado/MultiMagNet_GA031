from mnist import MNIST
from abc import ABC, abstractmethod
from pathlib import Path
from hashlib import sha256
import json

class ImageDAO:
    @staticmethod
    def get_images(training=True):
        mnist_data = MNIST("data/images")
        if training:
            images, labels = mnist_data.load_training()
        else:
            images, labels = mnist_data.load_testing()

        # print(mnist_data.display(images[index]))
        return images, labels

class UserDAO:
    def __init__(self):
        self.__path = "data/users/users.json"
        users_file_path = Path(self.__path)

        if users_file_path.exists():
            with open(self.__path, 'r') as users_file:
                try:
                    self.__users = json.load(users_file)
                except json.JSONDecodeError:
                    users_file.close()
                    with open(self.__path, 'w') as users_file:
                        self.__users = {}
                        self.__users[0] = ['0', '0']
                        json.dump(self.__users, users_file)
        else:
            with open(self.__path, 'w') as users_file:
                json.dump(self.__users, users_file)

    def get_user(self, id): 
        if str(id) in self.__users:
            return id, self.__users[str(id)]
        else:
            print("User with ID {0} not found.".format(id))
            return None

    def update_user(self, user):
        if user.id in self.__users:
            user_file = self.__users[user.id]
            self.__users[user.id].pop()

            user_file[0] = user.name
            user_file[1] = sha256(user_file.password).hexdigest()            
            
            self.__users[user.id] = user_file
            with open(self.__path, 'w') as users_file:
                json.dump(self.__users, users_file)
            return True
        else:
            print("User {0} not found.".format(id))
            return False

    def create_user(self, name, password):
        id = max(list(map(int, self.__users.keys())))+1
        hash = sha256(password.encode('utf-8')).hexdigest()
        self.__users[id] = [name, hash]
        
        with open(self.__path, 'w') as users_file:
            json.dump(self.__users, users_file)
            print("User {0} has been successfully inserted.".format(name))

        return True

    def get_users_size(self):
        return len(self.__users)