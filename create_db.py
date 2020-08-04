import psycopg2


class DatabaseCreation:

    @staticmethod
    def create_db(database_name):
        try:
            sql_db_create = 'CREATE DATABASE %s;', (database_name)
            return sql_db_create
        except psycopg2.Error.DuplicateDatabase:
            return "Database exist!"

    @staticmethod
    def create_user_table():
        try:
            sql_table = 'CREATE TABLE %s(%s serial primary key, \
                %s varchar(255), %s varchar(80));', ('Users', 'id', 'username', 'hashed_password')
            return sql_table
        except psycopg2.Error.DuplicateDatabase:
            return "Database exists!"
            
    @staticmethod
    def create_msg_table():
        try:
            sql_table = 'CREATE TABLE %s(%s serial primary key, \
                %s int not null, %s int not null, %s timestamp not null) \
                FOREIGN KEY(%s) REFERENCES Users(id) \
                FOREGIN KEY(%s) REFERENCES Users(id);', ('Messeges', 'id', 'from_id', 'to_id', 'creation_date', 'from_id', 'to_id')
            return sql_table
        except psycopg2.Error.DuplicateDatabase:
            return "Database exists!"
