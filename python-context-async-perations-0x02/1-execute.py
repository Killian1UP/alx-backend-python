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
            print("Connection closed")
            
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery('users.db', query, params) as results:
    for row in results:
        print(row)