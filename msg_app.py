if __name__ == '__main__':

    import argparse, models, hashlib_coders, psycopg2
    from datetime import datetime

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

    user1 = models.User.load_user_by_id(23, cursor)
    user2 = models.User.load_user_by_username("Marek", cursor)

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


    