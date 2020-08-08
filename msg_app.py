if __name__ == '__main__':

    import argparse, models, hashlib_coders, datetime, psycopg2

    #args for messeges
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='username')
    parser.add_argument('-p', '--password', help='password; must be at least 8 hcaracters long.')
    parser.add_argument('-l', '--list', action='store_true' ,help='list all users')
    parser.add_argument('-s', '--send', help="send inputed message")
    parser.add_argument('-t', '--to', help='send to user')



    connection = psycopg2.connect(
            user='postgres',
            password='@DoMInio1@', 
            host='localhost', 
            database='workshop')
    cursor = connection.cursor()


    #list containing all users in database
    base_of_users = models.User.load_all_users(cursor)

    def list_messages(user, cursor):
        sql = 'SELECT from_id, creation_date, msg FROM Messages WHERE to_id = %s;'
        cursor.execute(sql, user.get_id)
        messages = cursor.fetchall()
        return f'Messages send to user: {user.username}'messages
    

    def send_message(from_user, to_user, text):
        from_id = from_user.get_id
        to_id = to_user.get_id
        message = models.Messages(from_id, to_id, text)
        message.set_date(datetime.datetime.now())
        message.save_to_db(cursor)
        return f"Message send to user: {to_user}"