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
            sql = '''UPDATE INTO Users(username, hashed_password) VALUES (%s, %s)
            WHERE id = %s'''
            sql_values = (self.username, self._hashed_password, self._id)
            cursor.execute(sql, sql_values)
            return True

    @staticmethod
    def load_user_by_id(id_, cursor):
        sql = 'SELECT id, username, hashed_password FROM Users WHERE id = %s' % id_
        cursor.execute(sql)
        users_data = cursor.fetchone()
        if users_data:
            id_, username, hashed_password = users_data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None
    
    @staticmethod
    def load_user_by_username(username, cursor):
        sql = 'SELECT id, username, hashed_password FROM Users WHERE username = %s' % username
        cursor.execute(sql)
        users_data = cursor.fetchone()
        if users_data:
            id_, username, hashed_password = users_data
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None
    
    @staticmethod
    def load_all_users(cursor):
        sql = 'SELECT id, username, hashed_password FROM Users'
        users = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, username, hashed_password = row
            loaded_user = User(username)
            loaded_user._id = id_
            loaded_user._hashed_password = hashed_password
            users.append(loaded_user)
        return users

    def delete_user(self, cursor):
        sql = 'DELETE FROM Users WHERE id = %s' % self._id
        cursor.execute(sql)
        self._id = -1
        return True


# class Messages:

#     def __init__(self, )









if __name__ == "__main__":
    connection = psycopg2.connect(
        user='postgres',
        password='@DoMInio1@', 
        host='localhost', 
        database='workshop')
    cursor = connection.cursor()
