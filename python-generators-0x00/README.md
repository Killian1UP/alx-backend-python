# alx-backend-python

# MySQL Database Seeder – ALX_prodev

## 🎯 Objective

This project sets up a MySQL database called `ALX_prodev` and populates it with user data from a CSV file. It is designed to demonstrate database creation, table setup, and inserting data from a CSV file using Python.

---

## 📂 Files Included

- `seed.py` – Main Python script containing all database functions and logic
- `user_data.csv` – CSV file containing sample user data
- `.env` – Environment variables file (used to securely load DB credentials)

---

## 🧱 Database and Table Structure

### Database: `ALX_prodev`

### Table: `user_data`

| Field Name | Type         | Constraints                |
|------------|--------------|----------------------------|
| `user_id`  | CHAR(36)     | PRIMARY KEY, UUID, INDEXED |
| `name`     | VARCHAR(100) | NOT NULL                   |
| `email`    | VARCHAR(130) | NOT NULL                   |
| `age`      | DECIMAL      | NOT NULL                   |

---

## ⚙️ Function Prototypes

### `def connect_db():`
- Connects to the MySQL database server (without selecting a DB).
- Uses credentials stored in a `.env` file.

### `def create_database(connection):`
- Creates the `ALX_prodev` database if it doesn't exist.

### `def connect_to_prodev():`
- Connects specifically to the `ALX_prodev` database.

### `def create_table(connection):`
- Creates the `user_data` table inside `ALX_prodev` if it doesn't exist.
- Includes proper constraints for `UUID`, `NOT NULL`, and `INDEX`.

### `def insert_data(connection, csv_path):`
- Reads the CSV file `user_data.csv`.
- Inserts users into the `user_data` table if their email is not already present (prevents duplicates).
- Generates `UUID` for each new user.

---

## 🧪 Sample Usage

```python
if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    conn = connect_to_prodev()
    if conn:
        create_table(conn)
        insert_data(conn, "user_data.csv")
        conn.close()
