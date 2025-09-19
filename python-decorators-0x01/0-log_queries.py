import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query', None)
        if query is None:
            for a in args:
                if isinstance(a,str):
                    query = a
                    break
                
        if query is not None:
            print("[LOG] Executing sql query:", query)
        else:
            print("[LOG] No sql query found")
        return func(*args, **kwargs)
    return wrapper
        

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
