from hashlib_coders import hash_password
import psycopg2


#TO DO -> Opisy!!!!
#Dokończyć doksy do każdej funkcji 

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
        
        """
        Saves user to db or updates if there is user with that parameters
        """
        
        if self._id == -1:
            sql = '''INSERT INTO Users(username, hashed_password) VALUES (%s, %s)
            RETURNING id'''
            sql_values = (self.username, self._hashed_password)
            cursor.execute(sql, sql_values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = '''UPDATE Users SET username = %s, hashed_password = %s
            WHERE id = %s'''
            sql_values = (self.username, self._hashed_password, self._id)
            cursor.execute(sql, sql_values)
            return True

    def delete_user(self, cursor):
        """Deletes user from table"""
        
        sql = 'DELETE FROM Users WHERE id = %s'
        cursor.execute(sql, (self._id, ))
        self._id = -1
        return True

    @staticmethod
    def load_user_by_id(id_, cursor):
        """Loads user by id.
        Return User object with parameters taken form table
        """

        sql = 'SELECT id, username, hashed_password FROM Users WHERE id = %s'
        cursor.execute(sql, (id_, ))
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
        """Loads user by username.
        Returns User object with parameters taken form table"""

        sql = 'SELECT id, username, hashed_password FROM Users WHERE username = %s' 
        cursor.execute(sql, (username, ))
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
        """Loads all users in table.
        Returns list of User objects"""

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


class Messages:

    def __init__(self, from_id="", to_id="", text=''):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = "Nic"

    @property
    def get_id(self):
        """Returns id of a message"""

        return self._id

    def save_to_db(self, cursor):
        """Saves object or, if exists, updates object at Messages table"""
    
        if self._id == -1:
            sql = '''INSERT INTO Messages(from_id, to_id) VALUES (%s, %s)
            RETURNING id''' 
            sql_values = (self.from_id, self.to_id)
            cursor.execute(sql, sql_values)
            self._id = cursor.fetchone()[0]
            return True
        else:
            sql = '''UPDATE Messages SET from_id = %s, to_id = %s
            WHERE id = %s'''
            sql_values = (self.from_id, self.to_id, self._id)
            cursor.execute(sql, sql_values)
            return True

    @staticmethod
    def load_all_messages(cursor):
        """Loads all messages in table
        Returns list of Message obejcts"""

        sql = 'SELECT id, from_id, to_id, creation_date FROM Messages'
        messages = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            id_, from_id, to_id, creation_date = row
            loaded_msg = Messages()
            loaded_msg._id = id_
            loaded_msg.from_id = from_id
            loaded_msg.to_id = to_id
            loaded_msg.creation_date = creation_date
            messages.append(loaded_msg)
        return messages




if __name__ == "__main__":
    connection = psycopg2.connect(
        user='postgres',
        password='@DoMInio1@', 
        host='localhost', 
        database='workshop')
    cursor = connection.cursor()
