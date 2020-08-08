import psycopg2, psycopg2.errors as pg_err

class DatabaseCreation:
    """
    Class made to contain methods for database and table cration for
    python workshop
    """
    @staticmethod
    def create_db(database_name, cursor):
        """Creates database for project."""

        sql_db_create = 'CREATE DATABASE %s;'
        cursor.execute(sql_db_create, (database_name, ))
        return True


    @staticmethod
    def create_user_table(cursor):
        """creates "Users" table in db."""

        sql_table = """CREATE TABLE %s(%s serial primary key, \n
            %s varchar(255), %s varchar(80));"""
        values = ('Users', 'id', 'username', 'hashed_password')
        cursor.execute(sql_table, values)
        return True

    @staticmethod
    def create_msg_table(cursor):
        """creates "Messages" table in db."""

        sql_table = '''CREATE TABLE %s(%s serial primary key, \n
            %s int not null, %s int not null, %s timestamp, \n
            %s varchr(255), \n
            FOREIGN KEY(%s) REFERENCES Users(id), \n
            FOREIGN KEY(%s) REFERENCES Users(id)); ''' 
        values =  ('Messages', 'id', 'from_id', 'to_id', 'creation_date', 'msg', 'from_id', 'to_id')
        cursor.execute(sql_table, values)
        return True


# if __name__ == '__main__':
#     try:
#         connection = psycopg2.connect(
#             user='postgres',
#             password='@DoMInio1@', 
#             host='localhost', 
#             database='workshop')

#         cursor = connection.cursor()
#         cursor.execute(DatabaseCreation.create_msg_table())
#         connection.commit()
#     except Exception as e:
#         print(e)
#     else:
#         cursor.close()
#         connection.close()