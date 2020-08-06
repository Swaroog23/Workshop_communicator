import psycopg2, psycopg2.errors as pg_err

class DatabaseCreation:

    @staticmethod
    def create_db(database_name):
        sql_db_create = 'CREATE DATABASE %s;', (database_name)
        return sql_db_create

    @staticmethod
    def create_user_table():
        sql_table = ("""CREATE TABLE %s(%s serial primary key, \n
            %s varchar(255), %s varchar(80));""") % ('Users', 'id', 'username', 'hashed_password')
        return sql_table

    @staticmethod
    def create_msg_table():
        sql_table = '''CREATE TABLE %s(%s serial primary key, \n
            %s int not null, %s int not null, %s timestamp, \n
            FOREIGN KEY(%s) REFERENCES Users(id), \n
            FOREIGN KEY(%s) REFERENCES Users(id)); ''' % ('Messeges', 'id', 'from_id', 'to_id', 'creation_date', 'from_id', 'to_id')
        return sql_table


if __name__ == '__main__':
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='@DoMInio1@', 
            host='localhost', 
            database='workshop')

        cursor = connection.cursor()
        cursor.execute(DatabaseCreation.create_msg_table())
        connection.commit()
    except (psycopg2.OperationalError, pg_err.DuplicateTable) as error:
        print('ERROR OCCURED!  \n', error)
    else:
        cursor.close()
        connection.close()