if __name__ == '__main__':

    import argparse, models, psycopg2, hashlib_coders, create_db

    #args for users
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='username')
    parser.add_argument('-p', '--password', help='password; must be at least 8 hcaracters long.')
    parser.add_argument('-l', '--list', action='store_true' ,help='list all users')
    parser.add_argument('-e', '--edit', action='store_true', help='user edition')
    parser.add_argument('-n', '--new_pass', help='sets new password for a user')
    parser.add_argument('-d', '--delete', action="store_true", help="delete user")

    args = parser.parse_args()

    print(create_db.DatabaseCreation.create_db())

    #connection to db
    #if already exists, it informs user about it.
    connection = psycopg2.connect(
            user='postgres',
            password='@DoMInio1@', 
            host='localhost', 
            database='workshop')

    #Setting autocommit to True allows us to create databse if it does not exists
    connection.autocommit = True
    cursor = connection.cursor()

    print(create_db.DatabaseCreation.create_user_table(cursor))
    print(create_db.DatabaseCreation.create_msg_table(cursor))

    #Setting autocommit to False, because we dont need it anymore
    connection.autocommit = False

    #list containing all users in database
    base_of_users = models.User.load_all_users(cursor)
    
    
    def new_password(edited_user, cursor):
        """Function for changing users password.
        Takes loaded user from database and updates its hashed password to a new, given one."""
        
        edited_user.set_password(args.new_pass)
        edited_user.save_to_db(cursor)
        connection.commit()
        return f'New password set for user {args.username}!'
    
    
    def create_user(cursor):
        """Creates new user with a password, then uploads it into a database"""
        
        user = models.User(args.username, args.password)
        user.save_to_db(cursor)
        connection.commit()
        return 'User created!'
    

    def delete_user(deleted_user, cursor):
        """Deletes user from database"""
        
        deleted_user.delete_user(cursor)
        connection.commit()
        return 'User deleted!'


    #checks if username and password are correct, and changes password for given user
    if args.username in [usr.username for usr in base_of_users] and args.edit: 

        edited_user = models.User.load_user_by_username(args.username, cursor)
        
        if not hashlib_coders.check_password(args.password, edited_user.get_hashed_password):
            raise psycopg2.errors.UniqueViolation('Wrong password!')
        
        else:
            if args.new_pass == None or len(args.new_pass) < 8:
                raise psycopg2.errors.UniqueViolation('Password too short! Must be at least 8 characters long.')
            
            #checks if old password is same as the new, given password
            elif hashlib_coders.check_password(args.new_pass, edited_user.get_hashed_password):
                raise psycopg2.errors.UniqueViolation("New password cannot be the same as the old password!")
            
            else:
                print(new_password(edited_user, cursor))

    #checking if user exists in database when you want to edit users settings
    elif args.username not in [usr.username for usr in base_of_users] and args.edit:
        raise psycopg2.errors.UniqueViolation('User does not exist!')

    #deleting user
    elif args.username in [usr.username for usr in base_of_users] and args.delete:
        deleted_user = models.User.load_user_by_username(args.username, cursor)
        
        if not hashlib_coders.check_password(args.password, deleted_user.get_hashed_password):
            raise psycopg2.errors.UniqueViolation('Wrong password!')
        
        else:
            print(delete_user(deleted_user, cursor))

    #creating new user
    elif args.username != None:

        if args.username in [usr.username for usr in base_of_users]:
            raise psycopg2.errors.UniqueViolation("Username is taken! Select new username")
        
        elif args.password == None or len(args.password) < 8:
            raise ValueError('Password too short! Must be at least 8 characters long.')
        
        else:
            print(create_user(cursor))

    #listing all users in database
    elif args.list:
        for usr in base_of_users:
            print(usr.username)
    
    else:
        parser.print_help()

    connection.close()
