import sqlite3 
import functools

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            conn = sqlite3.connect('users.db')
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except sqlite3.Error as e:
            print(f'Database Error {e}')
            raise
        finally:
            if conn:
                conn.close()
    return wrapper

def transactional(func):
    @functools.wraps(func)
    def wrapper(conn,*args, **kwargs):
        try:
            cursor = conn.cursor()
            cursor.execute("BEGIN TRANSACTION")
            result = func(conn,*args,**kwargs)
            cursor.execute("COMMIT")
            return result
        except Exception as e:
            try:
                cursor.execute("ROLLBACK")
            except sqlite3.Error as rollback_error:
                print(f'There was an error rolling back {rollback_error}')
            print(f'Transaction error {e}')
            raise
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')