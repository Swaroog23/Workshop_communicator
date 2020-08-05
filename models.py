from hashlib_coders import hash_password
import psycopg2

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
        if self._id == -1:
            sql = '''INSERT INTO Users(username, hashed_password) VALUES (%s, %s)
            RETURNING id'''
            sql_values = (self.username, self._hashed_password)
            cursor.execute(sql, sql_values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            return False

if __name__ == "__main__":
    user1 = User("Zeta", "DupaMaćka")
    connection = psycopg2.connect(
        user='postgres',
        password='@DoMInio1@', 
        host='localhost', 
        database='workshop')
    cursor = connection.cursor()

    print(user1.save_to_db(cursor))

    print(user1.get_id)