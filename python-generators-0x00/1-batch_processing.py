import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def stream_users_in_batches(batch_size):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database='ALX_prodev'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_data")
        
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
            
    except Error as e:
        print(f"❌ Database error: {e}")
        
    finally: 
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
for batch in stream_users_in_batches(batch_size=50):
    print(f"New batch ({len(batch)} rows):")   
    for row in batch:                        
        print(row)
        
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            age = int(user[3])
            if age > 25:
                yield user
    return

for user in batch_processing(batch_size=50):
    print(user)

        
        
        
        

        
        