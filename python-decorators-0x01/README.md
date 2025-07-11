
# Python Database Decorators

This project demonstrates the use of Python decorators to manage and enhance database operations using `sqlite3`, `functools`, and `time`. Each section corresponds to a specific task related to database management and optimization.

---

## 0️⃣ Logging Database Queries

### ✅ Objective
Create a decorator that logs SQL queries executed by any function.

### 🧩 Solution Highlights
- Implemented `log_queries` decorator that prints the SQL query before execution.
- Helps in debugging and tracking SQL commands.

```python
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args:
            print(f"Executed SQL: {args[0]}")
        elif 'query' in kwargs:
            print(f"Executed SQL: {kwargs['query']}")
        return func(*args, **kwargs)
    return wrapper
```

---

## 1️⃣ Handle Database Connections with a Decorator

### ✅ Objective
Create a decorator that automatically handles opening and closing database connections.

### 🧩 Solution Highlights
- Implemented `with_db_connection` decorator.
- Opens a connection, passes it to the function, and ensures it's closed afterward.

```python
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper
```

---

## 2️⃣ Transaction Management Decorator

### ✅ Objective
Automatically commit or rollback database operations based on success or failure.

### 🧩 Solution Highlights
- `transactional` decorator wraps DB logic inside a transaction.
- Commits if no exception; otherwise, rolls back.

```python
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise
    return wrapper
```

---

## 3️⃣ Retry Decorator for Transient Errors

### ✅ Objective
Retry database operations if they fail due to transient errors (e.g., database is locked).

### 🧩 Solution Highlights
- Retries `sqlite3.OperationalError` with a delay.
- Useful for resilience in concurrent access scenarios.

```python
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    if "database is locked" in str(e):
                        print(f"Attempt {attempt} failed: {e}. Retrying in {delay}s...")
                        last_exception = e
                        time.sleep(delay)
                    else:
                        raise
            print("All retries failed.")
            raise last_exception
        return wrapper
    return decorator
```

---

## 4️⃣ Caching Database Query Results

### ✅ Objective
Avoid redundant DB calls by caching results based on query strings.

### 🧩 Solution Highlights
- `cache_query_results` decorator caches results using query as key.
- Returns cached result for repeated queries.

```python
_query_cache = {}

def cache_query_results(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        cache_key = query
        if cache_key in _query_cache:
            print(f"Cache hit for: {cache_key}")
            return _query_cache[cache_key]
        print(f"Cache miss for: {cache_key}")
        result = func(conn, query, *args, **kwargs)
        _query_cache[cache_key] = result
        return result
    return wrapper
```

---

## 🧪 Example Usage

Each decorator can be composed with others as needed:

```python
@with_db_connection
@retry_on_failure(retries=3, delay=2)
@transactional
@cache_query_results
def fetch_users(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()
```

---

## 📁 Requirements
- Python 3.x
- `sqlite3` (standard library)
- No external packages required

---

## 📌 Notes
- Designed for educational purposes.
- Best practices include adding logging, TTL to cache, or using production-level cache backends (e.g., Redis).