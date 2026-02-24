import sqlite3
from config import DB_PATH



def inspect_table(table_name):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # 1. Get the data (LIMIT 5 is like .head())
        cursor.execute(f"PRAGMA table_list")
        rows = cursor.fetchall()
        
        # 2. Get the headers
        # cursor.description returns a tuple of info, the first item is the name
        headers = [description[0] for description in cursor.description]
        
        print(f"--- Schema for {table_name} ---")
        print(f"Columns: {headers}")
        print("First 5 rows:")
        for row in rows:
            print(row)

def list_tables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables found:")
        for table in tables:
            print(table[0])

if __name__ == "__main__":
    list_tables()

# Let's check the table we need for the Router
#inspect_table("mapSolarSystemJumps")