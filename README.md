# Python Generators – Data Streaming & Processing Project

This project is part of the **ALX Backend Python curriculum**, focused on building efficient, memory-conscious data pipelines using **Python generators** and **MySQL**.

The overall goal was to interact with a database of user information in a way that avoids loading large datasets entirely into memory — instead, streaming or batching data when needed.

---

## 📁 Repository Structure

```
alx-backend-python/
├── python-generators-0x00/
│   ├── seed.py
│   ├── fetch.py
│   ├── 0-stream_users.py
│   ├── 1-batch_processing.py
│   ├── 2-lazy_paginate.py
│   ├── 4-stream_ages.py
│   └── user_data.csv
```

---

## 🧩 Project Overview & Task Breakdown

---

### ✅ **Task 1: Database Setup and Seeding**

**Objective:** Prepare the MySQL database and populate it with data.

- **Database:** `ALX_prodev`
- **Table:** `user_data`
- **Schema:**
  - `user_id` – UUID (Primary Key, Indexed)
  - `name` – `VARCHAR`, NOT NULL
  - `email` – `VARCHAR`, NOT NULL
  - `age` – `DECIMAL`, NOT NULL

**Data Source:** [user_data.csv](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2024/12/3888260f107e3701e3cd81af49ef997cf70b6395.csv)

**Implemented in:** `seed.py`

---

### ✅ **Task 2: Stream Data Row-by-Row**

**Objective:** Create a generator that streams rows one at a time from the database using `yield`.

**Highlights:**
- Efficient memory usage by not loading all rows at once.
- Generator function: `stream_users()`

**Implemented in:** `0-stream_users.py`

---

### ✅ **Task 3: Batch Processing with Generators**

**Objective:** Fetch and process users in configurable batches.

**Highlights:**
- Batch user data using `LIMIT` and `OFFSET`.
- Process only users above age 25 using a `WHERE` clause.
- Generator function: `batch_processing(batch_size)`

**Implemented in:** `1-batch_processing.py`, with testing in `main.py`

---

### ✅ **Task 4: Lazy Pagination**

**Objective:** Simulate fetching paginated data lazily using a generator.

**Highlights:**
- Implemented `lazy_paginate(page_size)` to fetch rows page-by-page.
- Ensures rows are only fetched when needed.
- Used `LIMIT` and `OFFSET` to simulate pagination.

**Implemented in:** `2-lazy_paginate.py`

---

### ✅ **Task 5: Streaming Aggregation – Average Age**

**Objective:** Use a generator to compute the average age of users **without using SQL's `AVG()`**.

**Highlights:**
- Stream ages using `stream_user_ages()` to avoid full memory load.
- Loop through data to compute aggregate (average).
- Print formatted result: `Average age of users: XX.XX`

**Implemented in:** `4-stream_ages.py`

---

## 🧪 Technologies Used

- **Python 3.12**
- **MySQL 8+**
- **mysql-connector-python**
- **python-dotenv** (for managing credentials securely via `.env` file)

---

## 🧼 Good Practices Followed

- Use of `.env` to protect sensitive database credentials.
- Clean separation of logic into modular scripts.
- Consistent use of `try/finally` blocks or `context managers` to manage database resources.
- Avoided memory overload by leveraging Python generators across all data access patterns.

---

## 🚀 Final Note

This project demonstrates the practical power of generators in building scalable, efficient systems that interact with databases — especially when handling large datasets or integrating pagination, batching, and custom aggregations.