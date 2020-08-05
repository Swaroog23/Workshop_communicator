from hashlib_coders import hash_password
import pscopg2

class User:
    '''
    User class related to users table in workshop database.
    Allows for creation of a user with hashed password, username,
    and id which is given by the database, while creating object,
    id is set to -1, so it cannot create problems with database
    '''
    
    def __init__(self, username="", password="", salt=None):
        self._id = -1
        self.username = username
        self._hashed_password = hash_password(password, salt)

    @property
    def get_id(self):
        
        """Id getter of a given object"""

        return self._id


    @property
    def get_hashed_password(self):
        
        """Password getter of a given object.
         Returns hashed password"""
        
        return self._hashed_password
    
    def set_password(self, password, salt=None):
        
        """Setter for _hashed_password.
        Gets new password, hashes it and updates objects __init__"""
        
        self._hashed_password = hash_password(password, salt)

    def save_to_db(self, cursor):
        pass

if __name__ == "__main__":
    user1 = User("Zeta", "DupaMaćka")
    print(user1.get_hashed_password)
    user1.set_password("GrubePaluchy1234")
    print(user1.get_hashed_password)