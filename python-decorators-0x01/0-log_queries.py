import sqlite3
import functools 
from datetime import datetime

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        if args:
            print(f"{timestamp} Executed SQL: {args[0]}")
        elif 'query' in kwargs:
            print(f"{timestamp} Executed SQL: {kwargs['query']}")
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
            email TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", [
            ('Ikaelelo', 'ika@email.com', 26),
            ('Lesedi', 'lesedi@email.com', 23),
            ('Jane', 'jane@email.com', 40),
            ('Patrick', 'pat@email.com', 63),
            ('Constance', 'constance@email.com', 58),
            ('Itumeleng', 'itu@email.com', 35)
        ])
    conn.commit()
    conn.close()

setup_database()

users = fetch_all_users("SELECT * FROM users")

print("Users:")
for user in users:
    print(user)