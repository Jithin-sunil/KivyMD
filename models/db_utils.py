from models.db_main_utils import *

# General CRUD functions
def fetch_all_records(table_name):
    query = f"SELECT * FROM {table_name}"
    return fetch_all(query)

def fetch_record_by_id(table_name, record_id):
    query = f"SELECT * FROM {table_name} WHERE id = ?"
    return fetch_one(query, [record_id])

def insert_record(table_name, columns, values):
    columns_str = ", ".join(columns)
    placeholders = ", ".join(["?"] * len(values))
    query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    return insert(query, values)

def update_record(table_name, columns, values, record_id):
    set_clause = ", ".join([f"{col} = ?" for col in columns])
    query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
    return update(query, values + [record_id])

def delete_record(table_name, record_id):
    query = f"DELETE FROM {table_name} WHERE id = ?"
    return delete(query, [record_id])

def fetch_joined_records(from_table, join_table, join_condition, where_clause=None, params=None):
    query = f"""
        SELECT *
        FROM {from_table}
        INNER JOIN {join_table}
        ON {join_condition}
    """
    if where_clause:
        query += f" WHERE {where_clause}"
    return fetch_all(query, params)
