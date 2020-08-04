import psycopg2


def create_db(database_name):
    try:
        sql_db_create = 'CREATE DATABASE %s;', (database_name)
        return sql_db_create
    except psycopg2.Error.DuplicateDatabase:
        return "Database exist!"

def create_user_table():
    try:
        sql_table = 'CREATE TABLE %s(%s serial primary key, \
            %s varchar(255), %s varchar(80));', ('Users', 'id', 'username', 'hashed_password')
        return sql_table
    except psycopg2.Error.DuplicateDatabase:
        return "Database exists!"