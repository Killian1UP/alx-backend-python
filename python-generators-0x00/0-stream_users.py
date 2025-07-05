import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def stream_users():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True, buffered=False)
        cursor.execute("SELECT * FROM user_data")
    
        for row in cursor:
            yield row
    except Error as e:
        print(f"❌ Database error: {e}")
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
if __name__ == "__main__":
    for user in stream_users():
        print(user)