import psycopg2, psycopg2.errors as pg_err

class DatabaseCreation:
    """
    Class made to contain methods for database and table cration for
    python workshop
    """
    
    @staticmethod
    def create_db():
        """Creates database for project."""

        cnx = psycopg2.connect(
            user='postgres',
            password='Admin123', 
            host='localhost', 
            database='postgres')
        cnx.autocommit = True
        cursor = cnx.cursor()
        try:
            sql_db_create = 'CREATE DATABASE %s;' % 'Workshop'
            cursor.execute(sql_db_create)
            cnx.close()
            return True
        except psycopg2.errors.DuplicateDatabase as e:
            cnx.close()
            return e
        
    @staticmethod
    def create_user_table(cursor):
        """creates "Users" table in workshop database."""
        
        try:
            sql_table = """CREATE TABLE %s(%s serial primary key, \n
                %s varchar(255), %s varchar(80));""" % ('Users', 'id', 'username', 'hashed_password')
            cursor.execute(sql_table)
            return True
        except psycopg2.errors.DuplicateTable as e:
            return e
    
    @staticmethod
    def create_msg_table(cursor):
        """creates "Messages" table in workshop database."""
        
        try:
            sql_table = '''CREATE TABLE %s(%s serial primary key, \n
                %s int not null, %s int not null, %s timestamp, \n
                %s varchar(255), \n
                FOREIGN KEY(%s) REFERENCES Users(id) ON DELETE CASCADE, \n
                FOREIGN KEY(%s) REFERENCES Users(id)) ON DELETE CASCADE; '''  % ('Messages', 'id', 'from_id', 'to_id', 'creation_date', 'msg', 'from_id', 'to_id')
            
            cursor.execute(sql_table)
            return True
        
        except psycopg2.errors.DuplicateTable as e:
            return e


