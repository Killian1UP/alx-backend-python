
# SQLite Context Managers and Async Queries

This project demonstrates how to manage SQLite database connections and run queries efficiently using:

- ✅ Custom class-based context managers (`__enter__` and `__exit__`)
- ✅ Reusable query execution class
- ✅ Concurrent asynchronous queries using `aiosqlite` and `asyncio.gather`

---

## 0️⃣ Custom Class-Based Context Manager for DB Connection

**Objective**: Automatically open and close a SQLite connection using a context manager.

### ✅ `DatabaseConnection` class

```python
import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        print("Database connection opened.")
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
```

### 🔁 Usage

```python
with DatabaseConnection('users.db') as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)
```

---

## 1️⃣ Reusable Query Context Manager

**Objective**: Create a reusable class `ExecuteQuery` that executes a query with parameters and returns results.

### ✅ `ExecuteQuery` class

```python
import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(self.query, self.params)
            if self.query.strip().lower().startswith("select"):
                self.result = self.cursor.fetchall()
            else:
                self.conn.commit()
        except Exception as e:
            print(f"Query failed: {e}")
            self.conn.rollback()
            raise
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Connection closed.")
```

### 🔁 Usage

```python
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery('users.db', query, params) as results:
    for row in results:
        print(row)
```

---

## 2️⃣ Concurrent Asynchronous Database Queries

**Objective**: Run two queries concurrently using `aiosqlite` and `asyncio.gather`.

### ✅ Asynchronous functions

```python
import aiosqlite
import asyncio

async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All users:")
            return users

async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            users = await cursor.fetchall()
            print("All users older than 40:")
            return users

async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("\n👥 All Users:")
    for user in all_users:
        print(user)

    print("\n🧓 Users Older Than 40:")
    for user in older_users:
        print(user)

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
```

---

## ✅ Summary

- Used `__enter__` and `__exit__` to manage SQLite connections safely.
- Wrote reusable query execution logic.
- Ran multiple queries concurrently with async I/O.

---

**Enjoy clean, concurrent, and safe database operations!**