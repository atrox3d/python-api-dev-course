from datetime import datetime as dt
from schemas import Post, Posts


default_posts: Posts = [
    Post(title='default post 1', content='default content 1', id=1),
    Post(title='default post 2', content='default content 2', id=2)
]

