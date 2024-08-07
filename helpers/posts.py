from datetime import datetime as dt
from sqlite3 import Connection
from db import db
from models.post import Post, Posts


posts = Posts(posts=[
    Post(title='defaul post 1', content='default content 1', id=1, 
         created_at=dt.today().strftime('%Y-%m-%d %H:%M:%S')),
    Post(title='defaul post 2', content='default content 2', id=2,
         created_at=dt.today().strftime('%Y-%m-%d %H:%M:%S')),
])


def create_db_posts(conn:Connection, posts:Posts):
    for post in posts.posts:
        db.execute_sql(conn, '''
            INSERT INTO posts
            (title, content, published, created_at)
            VALUES
            (:title, :content, :published, :created_at)
        ''', **post.model_dump())

def get_db_posts(conn:Connection) -> Posts:
    conn.row_factory = db.dict_factory
    rows = db.execute_sql(conn, '''
        SELECT * FROM posts
    ''')
    posts = [Post(**row) for row in rows]
    return Posts(posts=posts)
