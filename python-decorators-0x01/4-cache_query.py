import time
import sqlite3 
import functools


query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn,query):
        if query in query_cache:
            return query_cache[query]
        
        result = func(conn,query)
        query_cache[query] = result
        return result
    return wrapper
    
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
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
