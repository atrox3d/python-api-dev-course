from contextlib import closing
import sqlite3
from sqlite3 import Connection, Cursor
from db import sql

def dict_factory(connection, row) -> dict:
    return {
            col[0]: row[idx] 
            for idx, col in enumerate(connection.description)
    }

def get_connection(file_path:str) -> Connection:
    return sqlite3.connect(file_path)

def setup_db(filepath:str, tablename:str) -> Connection:
    conn = get_connection(filepath)
    drop_table(conn, tablename)
    create_table(conn, tablename)
    return conn

def drop_table(conn:Connection, tablename:str) -> Cursor:
    with conn:
        with closing(conn.cursor()) as cur:
            return cur.execute(sql.drop_table.format(tablename))

def create_table(conn:Connection, tablename:str) -> Cursor:
    with conn:
        with closing(conn.cursor()) as cur:
            cur.execute(sql.create_table.format(tablename))

def execute_sql(conn:Connection, sql:str, **data) -> Cursor:
    with conn:
        with closing(conn.cursor()) as cur:
            return cur.execute(sql, data)

