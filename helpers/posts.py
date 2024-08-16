from datetime import datetime as dt
from schemas import PostBase, Posts


default_posts: Posts = [
    PostBase(title='default post 1', content='default content 1'),
    PostBase(title='default post 2', content='default content 2')
]

