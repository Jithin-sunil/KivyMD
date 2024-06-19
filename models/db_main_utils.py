# db_main_utils.py
import sqlite3

def create_connection():
    return sqlite3.connect('data/db_kivy.db')

def execute_query(query, params=None, fetch=False):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        if fetch:
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.commit()
        return cursor.rowcount

def fetch_all(query, params=None):
    return execute_query(query, params, fetch=True)

def fetch_one(query, params=None):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params or [])
        row = cursor.fetchone()
        if row:
            columns = [col[0] for col in cursor.description]
            return dict(zip(columns, row))
        return None

def insert(query, params=None):
    return execute_query(query, params)

def update(query, params=None):
    return execute_query(query, params)

def delete(query, params=None):
    return execute_query(query, params)

def create_table(query):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()

def ensure_tables_exist():
    tables = [
        """
        CREATE TABLE IF NOT EXISTS districts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """,
       """
       CREATE TABLE IF NOT EXISTS tbl_category (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL  
        )
       """,
    ]
    for table_query in tables:
        create_table(table_query)