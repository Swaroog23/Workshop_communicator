if __name__ == '__main__':

    import argparse, models, psycopg2, hashlib_coders, create_db


    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='username')
    parser.add_argument('-p', '--password', help='password; must be at least 8 hcaracters long.')
    parser.add_argument('-l', '--list', action='store_true' ,help='list all users')
    parser.add_argument('-e', '--edit', action='store_true', help='user edition')
    parser.add_argument('-n', '--new_pass', help='sets new password for a user')
    parser.add_argument('-d', '--delete', action="store_true", help="delte user")


    args = parser.parse_args()
    
    try:
        connection = psycopg2.connect(
            user='postgres',
            password='@DoMInio1@', 
            host='localhost', 
            database='workshop')
        cursor = connection.cursor()
    except Exception as e:
        print(e)
    except (psycopg2.OperationalError, psycopg2.errors.DuplicateTable) as error:
        print('ERROR OCCURED!  \n', error)



    base_of_users = models.User.load_all_users(cursor)
    
    #setting new password for the user
    if args.username in [usr.username for usr in base_of_users] and args.edit: 
        edited_user = models.User.load_user_by_username(args.username, cursor)
        if not hashlib_coders.check_password(args.password, edited_user.get_hashed_password):
            raise psycopg2.errors.UniqueViolation('Wrong password!')
        else:
            if args.new_pass == None or len(args.new_pass) < 8:
                raise psycopg2.errors.UniqueViolation('Password too short! Must be at least 8 characters long.')
            elif hashlib_coders.check_password(args.new_pass, edited_user.get_hashed_password):
                raise psycopg2.errors.UniqueViolation("New password cannot be the same as the old password!")
            else:
                edited_user.set_password(args.new_pass)
                edited_user.save_to_db(cursor)
                connection.commit()
                print(f'New password set for user {args.username}!')

    #checking if user exists in database when you want to edit users settings
    elif args.username not in [usr.username for usr in base_of_users] and args.edit:
        raise psycopg2.errors.UniqueViolation('User does not exist!')

    #deleting user
    elif args.username in [usr.username for usr in base_of_users] and args.delete:
        delete_user = models.User.load_user_by_username(args.username, cursor)
        if not hashlib_coders.check_password(args.password, delete_user.get_hashed_password):
            raise psycopg2.errors.UniqueViolation('Wrong password!')
        else:
            delete_user.delete_user(cursor)
            connection.commit()
            print('User deleted!')

    #creating new user
    elif args.username != None:
        if args.username in [usr.username for usr in base_of_users]:
            raise psycopg2.errors.UniqueViolation("Username is taken! Select new username")
        elif args.password == None or len(args.password) < 8:
            raise ValueError('Password too short! Must be at least 8 characters long.')
        else:
            user = models.User(args.username, args.password)
            user.save_to_db(cursor)
            connection.commit()
            print('User created!')

    #listing all users in database
    if args.list:
        for usr in base_of_users:
            print(usr.username)




