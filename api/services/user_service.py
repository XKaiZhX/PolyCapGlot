'''
ABC es una libreria para definir clases abstractas, el motivo del porque hacemos ésto
es porque no existen interfaces en python, así que la siguiente manera de implementar
la idea de interfaz sería con la herencia de una clase abstracta
'''

from abc import abstractmethod 
from abc import ABCMeta

from extensions import db
from utils.service_utils import generate_password_salt, generate_password_hash

class AbstractUserService(metaclass=ABCMeta):
    @abstractmethod
    def register(self, username:str, email:str, password:str):
        pass

    @abstractmethod
    def delete(self, email: str):
        pass

    @abstractmethod
    def update_username(self, email:str, username:str):
        pass

    @abstractmethod
    def update_password(self, email:str, password:str):
        pass

    @abstractmethod
    def find_one(self, email:str):
        pass

    @abstractmethod
    def check_user_password(self, email:str, password:str):
        pass

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_username(self, username:str):
        pass

class UserService(AbstractUserService):
    def register(self, username, email, password):
        print("UserService - register:\t" + username + ", " + email + ", " + password)

        if db.find_user(email) is not None:
            return False

        salt = generate_password_salt()

        encrypted = generate_password_hash(password, salt)
        print("UserService - register:\t" + encrypted)

        db.insert_user(username, email, encrypted, salt)
        print("UserService - register:\tInserted")

        return True
    
    def delete(self, email: str):
        print("UserService - delete:\t" + email)

        return db.delete_user(email)

    def update_username(self, email:str, username:str):
        print("UserService - update_username:\t" + email, ", " + username)

        found = db.find_user(email)

        if found is None:
            return False

        return db.update_user_username(email, username)
        
    def update_password(self, email:str, password:str):
        print("UserService - update_password:\t" + email, ", " + password)

        found = db.find_user(email)

        if found is None:
            return False

        encrypted = generate_password_hash(password, found["salt"])
        print("UserService - register:\t" + encrypted)

        return db.update_user_password(email, encrypted)

    def find_one(self, email:str):
        return db.find_user(email)

    def check_user_password(self, email:str, password:str):
        found = self.find_one(email)
        if found is None:
            return False

        stored = found["password"]
        salt = found["salt"]

        encrypted = generate_password_hash(password, salt)

        return stored == encrypted

    def find_all(self):
        found = db.find_users()
        print("UserService - find_users:\t" + str(found))
        return found
    
    def find_by_username(self, username:str):
        found = db.find_by_username(username) 
        print("UserService - find_by_username:\t" + str(found))
        return found