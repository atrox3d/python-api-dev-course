from contextlib import closing
import sqlite3
from sqlite3 import Connection, Cursor
from datetime import datetime as dt

from models.post import Post, Posts


def dict_factory(connection, row) -> dict:
    return {
            col[0]: row[idx] 
            for idx, col in enumerate(connection.description)
    }

def get_connection(file_path:str) -> Connection:
    return sqlite3.connect(file_path, check_same_thread=False)

def setup_db(filepath:str, tablename:str) -> Connection:
    conn = get_connection(filepath)
    drop_table(conn, tablename)
    create_table(conn, tablename)
    return conn

def drop_table(conn:Connection, tablename:str):
    with conn:
        with closing(conn.cursor()) as cur:
            return cur.execute('DROP TABLE IF EXISTS {}'.format(tablename))

def create_table(conn:Connection, tablename:str):
    with conn:
        with closing(conn.cursor()) as cur:
            cur.execute('''
                    CREATE TABLE {} (
                        id INTEGER PRIMARY KEY,
                        title VARCHAR(50) NOT NULL,
                        content VARCHAR(500) NOT NULL,
                        published INTEGER NOT_NULL,
                        created_at TEXT NOT NULL
                    )
                '''.format(tablename))

def execute_sql(conn:Connection, sql:str, **data) -> list:
    # print(f'EXECUTE_SQL | {sql = }')
    with conn: # commit
        with closing(conn.cursor()) as cur:
            # result = cur.execute(sql, data).fetchall()
            # cur.execute() returns self
            cur.execute(sql, data)
            result = cur.fetchall()
            print(f'EXECUTE_SQL | fetchall {result = }')
            return result

def create_db_post(conn:Connection, post:Post):
        execute_sql(conn, '''
            INSERT INTO posts
            (title, content, published, created_at)
            VALUES
            (:title, :content, :published, :created_at)
        ''', **post.model_dump())

def create_db_posts(conn:Connection, posts:Posts):
    for post in posts.posts:
        create_db_post(conn, post)

def get_db_posts(conn:Connection) -> Posts:
    conn.row_factory = dict_factory
    rows = execute_sql(conn, '''
        SELECT * FROM posts
    ''')
    posts = [Post(**row) for row in rows]
    return Posts(posts=posts)

def find_db_post(conn:Connection, id:int) -> Post | None:
    conn.row_factory = dict_factory
    rows = execute_sql(conn, '''
        SELECT * FROM posts
        WHERE id = :id
    ''', id=id)
    if rows:
        return Post(**rows[0])
