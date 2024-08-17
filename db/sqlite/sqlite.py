from contextlib import closing
import sqlite3
from sqlite3 import Connection, Cursor
from datetime import datetime as dt
import logging

import schemas.post as post

# from schemas.schemas import Post, Posts
# from schemas import Post, Posts

logger = logging.getLogger(__name__)

def logged(fn):
    def wrap(*args, **kwargs):
        logger.debug(f'{fn.__name__} | {args=}, {kwargs=}')
        result = fn(*args, **kwargs)
        logger.debug(f'{fn.__name__} | {result=}')
        return result
    return wrap

@logged
def dict_factory(connection, row) -> dict:
    return {
            col[0]: row[idx] 
            for idx, col in enumerate(connection.description)
    }

@logged
def get_connection(file_path:str) -> Connection:
    return sqlite3.connect(file_path, check_same_thread=False)

@logged
def setup_db(filepath:str, tablename:str) -> Connection:
    conn = get_connection(filepath)
    drop_table(conn, tablename)
    create_table(conn, tablename)
    return conn

@logged
def drop_table(conn:Connection, tablename:str):
    with conn:
        with closing(conn.cursor()) as cur:
            return cur.execute('DROP TABLE IF EXISTS {}'.format(tablename))

@logged
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

@logged
def execute_sql(conn:Connection, sql:str, **data) -> list:
    # print(f'EXECUTE_SQL | {sql = }')
    with conn: # commit
        with closing(conn.cursor()) as cur:
            # result = cur.execute(sql, data).fetchall()
            # cur.execute() returns self
            cur.execute(sql, data)
            result = cur.fetchall()
            # print(f'EXECUTE_SQL | fetchall {result = }')
            return result

@logged
def create_db_post(conn:Connection, post:post.PostCreate):
        execute_sql(conn, '''
            INSERT INTO posts
            (title, content, published, created_at)
            VALUES
            (:title, :content, :published, :created_at)
        ''', **post.model_dump())

@logged
def create_db_posts(conn:Connection, posts:post.PostCreate):
    for post in posts.posts:
        create_db_post(conn, post)

@logged
def get_db_posts(conn:Connection) -> post.PostBase:
    conn.row_factory = dict_factory
    rows = execute_sql(conn, '''
        SELECT * FROM posts
    ''')
    posts = [post.PostBase(**row) for row in rows]
    return post.PostBase(posts=posts)

@logged
def find_db_post(conn:Connection, id:int) -> post.PostBase | None:
    conn.row_factory = dict_factory
    rows = execute_sql(conn, '''
        SELECT * FROM posts
        WHERE id = :id
    ''', id=id)
    if rows:
        return post.PostBase(**rows[0])

@logged
def delete_db_post(conn:Connection, id:int) -> post.PostBase | None:
    conn.row_factory = dict_factory
    rows = execute_sql(conn, '''
        DELETE FROM posts
        WHERE id = :id
    ''', id=id)

@logged
def update_db_post(conn:Connection, id:int, update:post.PostCreate) -> post.PostBase | None:
    conn.row_factory = dict_factory
    rows = execute_sql(conn, '''
        UPDATE posts
        SET title = :title, content = :content
        WHERE id = :id
    ''', **update)
