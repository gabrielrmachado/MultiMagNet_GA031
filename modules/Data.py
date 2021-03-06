from mnist import MNIST
from abc import ABC, abstractmethod
from pathlib import Path
from hashlib import sha256
import json
from Attacks import AttackAlgorithm, Attack
from enum import Enum

class Dataset(Enum):
    Training = 1
    Test = 2

class ImageDAO:
    @staticmethod
    def get_images(numberOfImages:int, dataset = Dataset.Training):
        mnist_data = MNIST("data/images")
        
        if dataset == Dataset.Training:
            images, labels = mnist_data.load_training()
        else:
            images, labels = mnist_data.load_testing()

        return images[:numberOfImages], labels[:numberOfImages]

    @staticmethod
    def get_Vdataset(numberOfImages:int, algorithm: AttackAlgorithm, **params):
        from random import sample
        import numpy as np, math
        
        attack = Attack()
        images = list(ImageDAO.get_images(numberOfImages))[0]
        attack.set_attack(images.copy(), algorithm, **params)
        adv_images = sample(attack.perform_attack(), len(images))
        images.extend(list(adv_images))

        labels = np.ones(len(images))
        labels[:(math.ceil(len(images)/2))] = 0

        return images, labels

class UserDAO:
    def __init__(self, path = "data/users/users.json"):
        self.__path = path
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
            return str(id), self.__users[str(id)]
        else:
            raise ValueError("User with ID {0} not found.".format(id))

    def update_user(self, id, new_name, new_password, new_priority):
        try:
            id_str, user_file = self.get_user(id)
            user_file[0] = new_name
            user_file[1] = sha256(new_password.encode('utf-8')).hexdigest()
            user_file[2] = new_priority
            self.__users[id_str] = user_file
            with open(self.__path, 'w') as file:
                json.dump(self.__users, file)
            
            print("Changes applied successfully!")
            return True
            
        except ValueError as e:
            print(e)
            return False

    def create_user(self, name, password, priority):
        id = str(max(list(map(int, self.__users.keys())))+1)
        hash = sha256(password.encode('utf-8')).hexdigest()
        self.__users[id] = [name, hash, priority]
        
        with open(self.__path, 'w') as users_file:
            json.dump(self.__users, users_file)
            print("User {0} has been successfully inserted.".format(name))

        return True

    def get_users_size(self):
        return len(self.__users)

    def delete_user(self, id):
        try:
            id_str, user = self.get_user(id)
            del self.__users[id_str]                
            with open(self.__path, 'w') as users_file:
                json.dump(self.__users, users_file)
                print("User {0} has been removed successfully.".format(user[0]))
            
            return True

        except ValueError as e:
            print(e)
            return False

# "Gabriel Resende Machado", "445566"
# "Sabrina", "sag_22311as"