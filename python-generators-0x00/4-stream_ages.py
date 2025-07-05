import seed

def stream_user_ages():
        connection = seed.connect_to_prodev()
        cursor = connection.cursor()
        cursor.execute(f"SELECT age FROM user_data")
        
        for row in cursor:
            yield float(row[0])
            
        cursor.close()
        connection.close()
        
def calculate_average_age():
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
        
    if count > 0:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")
        
    else:
        print("No users found.")
        
# if __name__ == '__main__':
#     calculate_average_age()