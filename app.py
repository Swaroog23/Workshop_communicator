if __name__ == '__main__':

    import argparse, models, psycopg2


    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='username')
    parser.add_argument('-p', '--password', help='password; must be at least 8 hcaracters long.')
    parser.add_argument('-l', '--list', action='store_true' ,help='list all users')
    parser.add_argument('-e', '--edit', action='store_true', help='user edition')
    parser.add_argument('-n', '-new_pass', help='sets new password for a user')



    args = parser.parse_args()

    connection = psycopg2.connect(
        user='postgres',
        password='@DoMInio1@', 
        host='localhost', 
        database='workshop')
    cursor = connection.cursor()

    base_of_users = models.User.load_all_users(cursor)
    
    if args.username in [usr.username for usr in base_of_users] and args.edit: 
         username = args.username
         

    elif args.username != None:
        if args.username in [usr.username for usr in base_of_users]:
            raise psycopg2.errors.UniqueViolation("Username is taken! Select new username")
        elif args.password == None or len(args.password) < 8:
            raise ValueError('Password too short! Must be at least 8 characters long.')
        else:
            user = models.User(args.username, args.password)
            user.save_to_db(cursor)
            connection.commit()



    if args.list:
        for usr in base_of_users:
            print(usr.username)




