import sqlite3
import functools 
import time

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            print(f"Executed SQL: {args[0]}")
        elif 'query' in kwargs:
            print(f"Executed SQL: {kwargs['query']}")
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

def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", [
            ('Ikaelelo', 'ika@email.com'),
            ('Lesedi', 'lesedi@email.com'),
            ('Jane', 'jane@email.com')
        ])
    conn.commit()
    conn.close()

setup_database()

users = fetch_all_users("SELECT * FROM users")

print("Users:")
for user in users:
    print(user)