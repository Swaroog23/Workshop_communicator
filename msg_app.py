if __name__ == '__main__':

    import argparse, models, hashlib_coders, psycopg2, create_db
    from datetime import datetime

    #args for messeges
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='username')
    parser.add_argument('-p', '--password', help='password; must be at least 8 hcaracters long.')
    parser.add_argument('-l', '--list', action='store_true' ,help='list all users')
    parser.add_argument('-s', '--send', help="send inputed message")
    parser.add_argument('-t', '--to', help='send to user')

    args = parser.parse_args()

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
    print(create_db.DatabaseCreation.create_db())
    print(create_db.DatabaseCreation.create_user_table(cursor))
    print(create_db.DatabaseCreation.create_msg_table(cursor))
    #Setting autocommit to False, because we dont need it anymore
    connection.autocommit = False


    #list containing all users in database
    base_of_users = models.User.load_all_users(cursor)

    def list_messages(user, cursor):
        sql = 'SELECT from_id, creation_date, msg FROM Messages WHERE to_id = %s;'
        cursor.execute(sql, (user.get_id, ))
        connection.commit()
        messages = []
        for row in cursor.fetchall():
            from_id, creation_date, msg = row
            info = f'Message from: {from_id} created at: {creation_date}, "{msg}"'
            messages.append(info)
        return f'Messages send to user: {user.username} \n{messages}'
    

    def send_message(from_user, to_user, text, date=datetime.now()):
        from_id = from_user.get_id
        to_id = to_user.get_id
        message = models.Messages(from_id, to_id, text)
        message.set_date(date)
        message.save_to_db(cursor)
        connection.commit()
        return f"Message send to user: {to_user.username}"


    if args.username in [usr.username for usr in base_of_users]:
        user = models.User.load_user_by_username(args.username, cursor)
        if hashlib_coders.check_password(args.password, user.get_hashed_password):
            
            if args.list:
                print(list_messages(user, cursor))

            elif args.send and args.to:
                
                if args.to in [usr.username for usr in base_of_users]:
                    reciver = models.User.load_user_by_username(args.to, cursor)
                    print(send_message(user, reciver, args.send))
                else:
                    raise psycopg2.errors.UniqueViolation('Reciving user does not exist!!')
            
            else:
                parser.print_help()

        else:
            raise psycopg2.errors.UniqueViolation('Wrong password!')
    else:
        raise psycopg2.errors.UniqueViolation('User does not exist!!')

    connection.close()