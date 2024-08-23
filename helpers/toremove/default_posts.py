from datetime import datetime as dt
from schemas.post import PostDefault, Post, Posts


default_posts: Posts = [
    PostDefault(title='default post 1', content='default content 1',
             owner_id=1),
    PostDefault(title='default post 2', content='default content 2',
             owner_id=1),
    PostDefault(title='bob post', content='default content 2',
             owner_id=2),
]
