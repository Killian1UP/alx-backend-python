import mysql.connector
from mysql.connector import Error
import uuid
import csv
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )
        if connection.is_connected():
            print("✅ Connected to MySQL database")
            return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None
    
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("✅ Database 'ALX_prodev' created or already exists")
        cursor.close()
    except Error as e:
        print(f"❌ Error creating database: {e}")
        
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("✅ Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"❌ Error connecting to ALX_prodev database: {e}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(130) NOT NULL,
            age DECIMAL NOT NULL
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("✅ Table 'user_data' created or already exists")
        cursor.close()
    except mysql.connector.Error as e:
        print(f"❌ Error creating table: {e}")
        
def insert_data(connection, csv_path):
        try:
            cursor = connection.cursor()
            with open(csv_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    name = row['name']
                    email = row['email']
                    age = row['age']

                    # Check if email already exists (prevent duplicates)
                    cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
                    existing = cursor.fetchone()
                    if existing:
                        print(f"⚠️ User with email {email} already exists. Skipping...")
                        continue

                    # Insert new record
                    user_id = str(uuid.uuid4())
                    insert_query = """
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (user_id, name, email, age))
                    print(f"✅ Inserted: {name} ({email})")
            
            connection.commit()
            cursor.close()
        except Exception as e:
            print(f"❌ Error inserting data: {e}")

    
if __name__ == "__main__":
    conn = connect_to_prodev()
    if conn:
        insert_data(conn, "user_data.csv")
        conn.close()